"""
Wraps OpenCV's :mod:`cv2` ``VideoCapture`` class, which supports many webcams and videostreams.
"""
import numpy as np
import cv2

from slmsuite.hardware.cameras.camera import Camera

class Webcam(Camera):
    """
    Wraps OpenCV's :mod:`cv2` ``VideoCapture`` class,
    which supports many webcams and videostreams.

    Warning
    -------
    This class does not properly handle color images 
    and does not properly populate datatype information.

    See Also
    --------
    `OpenCV documentation <https://docs.opencv.org/4.x/d8/dfe/classcv_1_1VideoCapture.html>`_.

    Attributes
    ----------
    cam : cv2.VideoCapture
        Most cameras will wrap some handle which connects to the the hardware.
    """

    def __init__(
        self,
        identifier=0,
        capture_api=cv2.CAP_ANY,
        pitch_um=None,
        verbose=True,
        **kwargs
    ):
        """
        Initialize camera and attributes.

        Parameters
        ----------
        identifier : int OR str
            Identity of the camera to open. This can be either an integer index
            (numbered by the OS) or a string URL of a videostream
            (e.g. ``protocol://host:port/script_name?script_params|auth``).
            The OS's default camera (index of ``0``) is used as the default.
        capture_api : int
            The ``cv2.VideoCaptureAPI`` to use for capturing.
            Defaults to ``cv2.CAP_ANY`` (choose OS default).
        pitch_um : (float, float) OR None
            Fill in extra information about the pixel pitch in ``(dx_um, dy_um)`` form
            to use additional calibrations.
        verbose : bool
            Whether or not to print extra information.
        **kwargs
            See :meth:`.Camera.__init__` for permissible options.
        """
        # Then we load the camera from the SDK
        id = f'{identifier}' if isinstance(identifier, str) else identifier
        if verbose: print(f"Webcam {id} initializing... ", end="")
        self.cam = cv2.VideoCapture(identifier, capture_api)
        if not self.cam.isOpened():
            raise RuntimeError(f"Failed to initialize webcam {id}")
        if verbose: print("success")

        # Finally, use the superclass constructor to initialize other required variables.
        super().__init__(
            (
                int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
            ),
            bitdepth=8,
            pitch_um=pitch_um,
            name=str(identifier),
            **kwargs
        )

        self.backend = self.cam.getBackendName()

    def close(self):
        """See :meth:`.Camera.close`."""
        self.cam.release()
        del self.cam

    @staticmethod
    def info(verbose=True):
        """Not supported by :class:`Webcam`."""
        raise NotImplementedError()

    ### Property Configuration ###

    def get_exposure(self):
        """See :meth:`.Camera.get_exposure`."""
        return 2**float(self.cam.get(cv2.CAP_PROP_EXPOSURE))

    def set_exposure(self, exposure_s):
        """See :meth:`.Camera.set_exposure`."""
        self.cam.set(cv2.CAP_PROP_EXPOSURE, np.log2(exposure_s))

    def _get_image_hw(self, timeout_s=1):
        """See :meth:`.Camera._get_image_hw`."""
        (success, img) = self.cam.read()
        if not success: raise RuntimeError("Could not grab frame.")
        img = np.array(img)
        if len(img.shape) == 3:
            return img[:,:,::-1]    # Flip BGR to RGB; FUTURE: Make more general.
        else:
            return img