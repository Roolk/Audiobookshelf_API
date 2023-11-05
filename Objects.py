from dataclasses import dataclass, asdict, fields
from typing import Optional, List, Union, Type

__all__ =['Library', 'Folder', 'LibrarySettings']

@dataclass()
class Base:
  def to_dict(self):
    return asdict(self)

  @classmethod
  def from_dict(cls, data):
    # Create a dictionary containing only the attributes defined in the class
    valid_data = {field.name: data[field.name] for field in fields(cls) if field.name in data}
    return cls(**valid_data)


@dataclass
class Library(Base):
  """
  Represents a library.

  Attributes:
      id (str): The ID of the library. (Read Only)
      name (str): The name of the library.
      folders (List[Folder]): The folders that the library is composed of on the server.
      displayOrder (int): Display position of the library in the list of libraries. Must be >= 1.
      icon (str): The selected icon for the library. See Library Icons for a list of possible icons.
      mediaType (str): The type of media that the library contains. Will be book or podcast. (Read Only)
      provider (str): Preferred metadata provider for the library. See Metadata Providers for a list of possible providers.
      settings (LibrarySettings): The settings for the library.
      createdAt (int): The time (in ms since POSIX epoch) when the library was created. (Read Only)
      lastUpdate (int): The time (in ms since POSIX epoch) when the library was last updated. (Read Only)
  """
  id: str
  name: str
  folders: List[Type['Folder']]
  displayOrder: int
  icon: str
  mediaType: str
  provider: str
  settings: Type['LibrarySettings']
  createdAt: int
  lastUpdate: int


@dataclass
class LibrarySettings(Base):
    """
    Represents library settings.

    Attributes:
        coverAspectRatio (int): Whether the library should use square book covers. Must be 0 (for false) or 1 (for true).
        disableWatcher (bool): Whether to disable the folder watcher for the library.
        skipMatchingMediaWithAsin (bool): Whether to skip matching books that already have an ASIN.
        skipMatchingMediaWithIsbn (bool): Whether to skip matching books that already have an ISBN.
        autoScanCronExpression (str or None): The cron expression for when to automatically scan the library folders.
            If None, automatic scanning will be disabled.
    """
    coverAspectRatio: int
    disableWatcher: bool
    skipMatchingMediaWithAsin: bool
    skipMatchingMediaWithIsbn: bool
    autoScanCronExpression: Optional[str]


'''class LibraryFilterData(Base):
  """
  Represents library filter data.

  Attributes:
      authors (List[AuthorMinified]): The authors of books in the library.
      genres (List[str]): The genres of books in the library.
      tags (List[str]): The tags in the library.
      series (List[Series]): The series in the library. The series will only have their id and name.
      narrators (List[str]): The narrators of books in the library.
      languages (List[str]): The languages of books in the library.
  """
  authors: List[AuthorMinified]
  genres: List[str]
  tags: List[str]
  series: List[Series]
  narrators: List[str]
  languages: List[str]'''


@dataclass
class Folder(Base):
  """
  Represents a folder.

  Attributes:
      id (str): The ID of the folder. (Read Only)
      fullPath (str): The path on the server for the folder. (Read Only)
      libraryId (str): The ID of the library the folder belongs to. (Read Only)
      addedAt (int): The time (in ms since POSIX epoch) when the folder was added. (Read Only)
  """
  id: Optional[str]
  fullPath: Optional[str]
  libraryId: Optional[str]
  addedAt: Optional[int]


'''@dataclass
class Book(Base):
  """
  Represents a book.

  Attributes:
      libraryItemId (str): The ID of the library item that contains the book.
      metadata (BookMetadata): The book's metadata.
      coverPath (str or None): The absolute path on the server of the cover file. Will be None if there is no cover.
      tags (list of str): The book's tags.
      audioFiles (list of AudioFile): The book's audio files.
      chapters (list of BookChapter): The book's chapters.
      missingParts (list of int): Any parts missing from the book by track index.
      ebookFile (EBookFile or None): The book's ebook file. Will be None if this is an audiobook.
  """
  libraryItemId: str
  metadata: BookMetadata
  coverPath: Optional[str]
  tags: List[str]
  audioFiles: List[AudioFile]
  chapters: List[BookChapter]
  missingParts: List[int]
  ebookFile: Optional[EBookFile]'''
