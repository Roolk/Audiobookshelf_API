import requests
from typing import List, Union, Optional
from Objects import *
from audiobookshelfenums import *
import json


class AudiobookshelfAPI:

    def __init__(self, url, api_token):
        self.api_token = api_token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_token
        }
        self.base_url = url
        self.api_url = self.base_url + "/api"
        self.libraries_url = self.api_url + '/libraries'
        self.items_url = self.api_url + '/items'
        if not self.ping():
            raise "Failed to ping server"

    def _send_get_request(self, url: str) -> requests.Response:
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            # Uncomment line below to print the response from the server
            print(json.dumps(response.json(),indent=2), response.status_code)
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON parsing error: {e}")

    def _send_patch_request(self, url: str, json_data: dict) -> requests.Response:
        try:
            response = requests.patch(url, headers=self.headers, json=json_data)
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request error: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"JSON parsing error: {e}")

    def ping(self):
        url = f"{self.base_url}/ping"
        response = self._send_get_request(url=url)
        return response.status_code == 200 and response.text == '{"success":true}'

    def create_library(self, name: str, folders_path: List[str], icon: Icon,
                       media_type: str, provider: Provider) -> Library:
        """
        Creates a new library with the provided attributes.

        Args:
            name (str): The name of the new library.
            folders_path (List[str]): A list of folder paths to be associated with the library.
            icon (Icon): The icon to be used for the new library.
            media_type (str): The type of media that the library will contain, either 'book' or 'podcast'.
            provider (Provider): The preferred metadata provider for the new library.

        Returns:
            Library: The newly created Library object.

        Raises:
            Exception: If the server responds with a status code other than 200, an exception is raised.

        Note:
            When updating folders you must pass in the full array of folders. Any missing folders from the array
             will be removed. New folders must not have an id set because this will be set automatically.

        Example:
            To create a new library with the specified attributes, you can call the method as follows:
            ```
            new_library = create_library(name='My New Library',
                                         folders_path=['/path/to/folder1', '/path/to/folder2'],
                                         icon=Icon.SOME_ICON,
                                         media_type='book',
                                         provider=Provider.SOME_PROVIDER)
            ```
        """
        url = self.libraries_url
        d = {}
        for folder in folders_path:
            d.update({'fullPath': folder})
        payload = {
            "name": name,
            "folders": [d],
            "icon": icon.value,
            "mediaType": media_type,
            "provider": provider.value
        }
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code != 200:
            print(json.dumps(payload, indent=2), response.text, response.reason, response.status_code)
            raise "Invalid Response from server. Failed to create library!"
        return Library.from_dict(json.loads(response.text))

    def get_all_libraries(self) -> List[Library]:
        """
        Get all the libraries in the Audiobookshelf instance
        Returns: (List[Library]) all libraries in Audiobookshelf instance

       """
        url = self.libraries_url
        response = self._send_get_request(url=url)
        return [Library.from_dict(library) for library in response.json()['libraries']]

    def get_library(self, library_id: str) -> Library:
        """
        Gets a library from its id

        Args:
          library_id: id of the library to get

        Returns: (Library) library from the provided id

        """
        url = f"{self.libraries_url}/{library_id}"
        response = self._send_get_request(url=url)
        return Library.from_dict(json.loads(response.text))

    def update_library(self,
                       id: str,
                       name: Optional[str] = None,
                       folders: Optional[List[Folder]] = None,
                       display_order: Optional[int] = None,
                       icon: Optional[Icon] = None,
                       provider: Optional[Provider] = None,
                       settings: Optional[LibrarySettings] = None) -> Library:
        """
        Update the library with the specified ID with new or modified attributes.

        Args:
            id (str): The ID of the library to be updated.
            name (Optional[str]): The updated name for the library.
            folders (Optional[List[Folder]]): A list of Folder objects representing the library's folders,
                                              must include all folders for the library.
            display_order (Optional[int]): The new display order for the library (must be >= 1).
            icon (Optional[Icon]): The updated icon for the library.
            provider (Optional[Provider]): The preferred metadata provider for the library.
            settings (Optional[LibrarySettings]): The updated settings for the library.

        Returns:
            Library: The updated Library object with the specified changes.

        Raises:
            Exception: If no fields to update are provided, an exception is raised.

        Note:
            The `id` parameter is required, and at least one of the optional parameters (e.g., `name`, `folders`,
             `display_order`, `icon`, `provider`, or `settings`) should be provided to make changes to the library.

        Example:
            To update the name of a library with ID 'abc123', you can call the method as follows:
            ```
            updated_library = update_library('abc123', name='New Library Name')
            ```
        """

        url = f"{self.libraries_url}/{id}"
        payload = {}
        if name is not None:
            payload["name"] = name
        if folders is not None:
            payload["folders"] = folders
        if display_order is not None:
            payload["displayOrder"] = display_order
        if icon is not None:
            payload["icon"] = icon
        if provider is not None:
            payload["provider"] = provider
        if settings is not None:
            payload["settings"] = settings

        if not payload:
            raise Exception("No fields to update")

        response = self._send_patch_request(url, json_data=payload)
        return Library.from_dict(response.json())

    def get_all_library_items(self, library_id: str) -> list[LibraryItem]:
        """
        Retrieve all library items for a specific library.

        Args:
            library_id (str): The ID of the library.

        Returns:
            List[LibraryItem]: A list of LibraryItem instances representing the library items.

        Raises:
            Exception: Raises an exception if the request to the server fails or if the response is invalid.
        """
        url = f"{self.libraries_url}/{library_id}/items"
        response = self._send_get_request(url)
        # print(json.dumps(response.json(), indent=2))
        return [LibraryItem.from_dict(item) for item in response.json()['results']]

    # untested
    def get_all_library_podcast_episode_downloads(self, library_id: str) -> List[PodcastEpisodeDownload]:
        url = f"{self.libraries_url}/{library_id}/episode-downloads"
        response = self._send_get_request(url)
        downloads = [PodcastEpisodeDownload.from_dict(response.json()['currentDownload'])]
        for download in response.json()['queue']:
            downloads.append(PodcastEpisodeDownload.from_dict(download))
        return downloads

    def get_library_series(self, library_id: str) -> List[SeriesBooks]:
        """
        Does not currently work due to error in server response?
        Args:
            library_id:

        Returns:

        """
        url = f"{self.libraries_url}/{library_id}/series"
        response = self._send_get_request(url)
        print(json.dumps(response.json(), indent=2))
        return [SeriesBooks.from_dict(result) for result in response.json()['results']]

    def get_library_collections(self, library_id: str) -> List[CollectionExpanded]:
        """
        Args:
            library_id:

        Returns:

        """
        url = f"{self.libraries_url}/{library_id}/collections"
        response = self._send_get_request(url)
        #Uncomment line to print response
        #print(json.dumps(response.json(), indent=2))
        return [CollectionExpanded.from_dict(result) for result in response.json()['results']]

    #tested?
    def get_user_playlists(self, library_id: str):
        url = f"{self.libraries_url}/{library_id}/playlists"
        response = self._send_get_request(url)
        return [PlaylistExpanded.from_dict(result) for result in response.json()['results']]

    def temp(self, itemID: str):
        url = f"{self.items_url}/{itemID}/media"
        response = self._send_patch_request(url, {})
        return response
