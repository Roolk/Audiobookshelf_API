import requests
from typing import List, Union, Optional
from Objects import *
from audiobookshelfenums import *
import json


class Audiobookshelf_API:

  def __init__(self, url, api_token):
    self.api_token = api_token
    self.headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + self.api_token
    }
    self.base_url = url
    self.api_url = self.base_url + "/api"
    self.libraries_url = self.api_url + '/libraries'
    if not self.ping(): raise ("Failed to ping server")

  def _send_get_request(self, url: str) -> requests.Response:
    try:
      response = requests.get(url, headers=self.headers)
      response.raise_for_status()  # Raise an exception for non-2xx status codes
      return response
    except requests.exceptions.RequestException as e:
      raise Exception(f"Request error: {e}")
    except json.JSONDecodeError as e:
      raise Exception(f"JSON parsing error: {e}")

  def ping(self):
    url = self.base_url + "/ping"
    response = requests.get(url, headers=self.headers)
    return response.status_code == 200 and response.text == '{"success":true}'

  def create_library(self, name: str, folders_path: List[str], icon: Icon,
                     media_type: str, provider: Provider) -> Library:
    """
    Creates a new library with the give arguments.

    Args:
      name: name of the library
      folders_path: the path of the folder for the new library
      icon: Icon to use for the new library
      media_type: book or podcast
      provider: Provider for the new library

    Returns: The Newly created library

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
    Get all the libraries in the audiobookshelf instance
    Returns: (List[Library]) all libraries in audiobookshelf instance

    """
    url = self.libraries_url
    response = requests.get(url, headers=self.headers)
    return [Library.from_dict(library) for library in response.json()['libraries']]

  def get_library(self, library_id: str) -> Library:
    url = f"{self.libraries_url}/{library_id}"
    response = self._send_get_request(url=url)
    return Library.from_dict(json.loads(response.text))


  def update_library(self,
                     library_or_id: Union[Library,  str],
                     name: Optional[str],
                     folders: List[Folder],
                     display_order: Optional[int],
                     icon: Optional[Icon],
                     provider: Optional[Provider],
                     settings: Optional[LibrarySettings]):

    if isinstance(library_or_id, str):
      # The provided argument is an ID, so fetch the library object
      url = self.libraries_url + "/" + library_or_id
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
    
    elif isinstance(library_or_id, Library):
      # The provided argument is a Library object
      url = self.libraries_url + "/" + library_or_id.id
      library = library_or_id
      
      payload = {
          "name": library.name,
          "folders": library.folders,
          "displayOrder": library.display_order,
          "icon": library.icon,
          "provider": library.provider,
          "settings": library.settings
      }

    response = requests.patch(url, headers=self.headers, json=payload)
    return Library.from_json(response.json())



def delete_library(self, id: str) -> Library:
  url = self.libraries_url + "/" + id
  response = requests.delete(url, headers=self.headers)
  return Library.from_json(response.json())


def get_all_library_items(self, library_id: str) -> list[Library]:
  url = self.libraries_url + "/" + library_id + "/items"
  response = requests.get(url, headers=self.headers)
  return [Library.from_json(library) for library in response.json()]
