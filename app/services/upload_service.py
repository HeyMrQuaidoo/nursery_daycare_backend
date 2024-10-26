import re
import uuid
import cloudinary
import cloudinary.api
import cloudinary.uploader

# utils
from app.core.config import settings
from app.core.response import DAOResponse


class MediaUploaderService:
    def __init__(self, base64_image, file_name, media_type="general"):
        self.base64_image = base64_image
        self.file_name = file_name
        self.media_type = media_type

    def get_image_type(self):
        """
        Extracts the image type from a base64 encoded image string.

        Args:
            base64_image (str): The base64 encoded image string.

        Returns:
            str: The image type (e.g., 'jpeg', 'png', 'gif') or None if not found.
        """
        # use regex to find the image type
        match = re.match(r"data:image/(?P<type>.+?);base64,", self.base64_image)
        if match:
            return match.group("type")
        return None

    def check_filename_exists(self):
        try:
            result = cloudinary.api.resources(type="upload", prefix=self.file_name)
            resources = result.get("resources", [])

            # check if the filename exists
            for resource in resources:
                if resource["public_id"] == self.file_name:
                    return True
            return False
        except Exception as e:
            print(f"Error checking file_name: {e}")
            return False

    def upload(self):
        # specify folder name
        folder_name = str(settings.APP_NAME + "/" + self.media_type + "/").lower()

        # replace spaces with underscore
        file_name = re.sub(r"\s+", "_", self.file_name)

        # TODO: Implement searching image information and returning it if already exists
        if self.check_filename_exists():
            file_name = file_name + "_" + str(uuid.uuid4())

        try:
            # upload an image
            upload_result = cloudinary.uploader.upload(
                self.base64_image,
                resource_type="auto",
                public_id=self.file_name,
                folder=folder_name,
            )

            # return upload_result['secure_url']
            return DAOResponse(
                success=True, data={"content_url": upload_result["secure_url"]}
            )
        except Exception as e:
            return DAOResponse(success=False, error=f"{str(e)}")
