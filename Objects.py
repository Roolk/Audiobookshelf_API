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
class Author(Base):
    """
    Represents an author.

    Attributes:
        id (str): The ID of the author.
        asin (str or None): The ASIN of the author. Will be None if unknown.
        name (str): The name of the author.
        description (str or None): A description of the author. Will be None if there is none.
        imagePath (str or None): The absolute path for the author image. Will be None if there is no image.
        addedAt (int): The time (in ms since POSIX epoch) when the author was added.
        updatedAt (int): The time (in ms since POSIX epoch) when the author was last updated.
    """
    id: str
    asin: Optional[str]
    name: str
    description: Optional[str]
    imagePath: Optional[str]
    addedAt: int
    updatedAt: int


@dataclass
class AuthorMinified(Base):
    """
    Represents an author.

    Attributes:
        id (str): The ID of the author.
        name (str): The name of the author.
    """
    id: str
    name: str


@dataclass
class AuthorExpanded(Base):
    """
    Represents an expanded author with additional information.

    Attributes:
        id (str): The ID of the author.
        asin (str or None): The ASIN of the author. Will be None if unknown.
        name (str): The name of the author.
        description (str or None): A description of the author. Will be None if there is none.
        imagePath (str or None): The absolute path for the author image. Will be None if there is no image.
        addedAt (int): The time (in ms since POSIX epoch) when the author was added.
        updatedAt (int): The time (in ms since POSIX epoch) when the author was last updated.
        numBooks (int): The number of books associated with the author in the library.
    """
    id: str
    asin: Optional[str]
    name: str
    description: Optional[str]
    imagePath: Optional[str]
    addedAt: int
    updatedAt: int
    numBooks: int


@dataclass
class BookMetadata(Base):
    """
    Represents metadata for a book.

    Attributes:
        title (str or None): The title of the book. Will be None if unknown.
        subtitle (str or None): The subtitle of the book. Will be None if there is no subtitle.
        authors (List[AuthorMinified]): The authors of the book.
        narrators (List[str]): The narrators of the audiobook.
        series (List[SeriesSequence]): The series the book belongs to.
        genres (List[str]): The genres of the book.
        publishedYear (str or None): The year the book was published. Will be null if unknown.
        publishedDate (str or None): The date the book was published. Will be null if unknown.
        publisher (str or None): The publisher of the book. Will be null if unknown.
        description (str or None): A description for the book. Will be null if empty.
        isbn (str or None): The ISBN of the book. Will be null if unknown.
        asin (str or None): The ASIN of the book. Will be null if unknown.
        language (str or None): The language of the book. Will be null if unknown.
        explicit (bool): Whether the book has been marked as explicit.
    """
    title: Optional[str]
    subtitle: Optional[str]
    authors: List[AuthorMinified]
    narrators: List[str]
    series: List[Type['SeriesSequence']]
    genres: List[str]
    publishedYear: Optional[str]
    publishedDate: Optional[str]
    publisher: Optional[str]
    description: Optional[str]
    isbn: Optional[str]
    asin: Optional[str]
    language: Optional[str]
    explicit: bool


@dataclass
class BookMetadataMinified(Base):
    """
    Represents metadata for a book with updated attributes.

    Attributes:
        titleIgnorePrefix (str): The title of the book with any prefix moved to the end.
        authorName (str): The name of the book's author(s).
        authorNameLF (str): The name of the book's author(s) with last names first.
        narratorName (str): The name of the audiobook's narrator(s).
        seriesName (str): The name of the book's series.
        title (str or None): The title of the book. Will be None if unknown.
        subtitle (str or None): The subtitle of the book. Will be None if there is no subtitle.
        genres (List[str]): The genres of the book.
        publishedYear (str or None): The year the book was published. Will be null if unknown.
        publishedDate (str or None): The date the book was published. Will be null if unknown.
        publisher (str or None): The publisher of the book. Will be null if unknown.
        description (str or None): A description for the book. Will be null if empty.
        isbn (str or None): The ISBN of the book. Will be null if unknown.
        asin (str or None): The ASIN of the book. Will be null if unknown.
        language (str or None): The language of the book. Will be null if unknown.
        explicit (bool): Whether the book has been marked as explicit.
    """
    titleIgnorePrefix: str
    authorName: str
    authorNameLF: str
    narratorName: str
    seriesName: str
    title: Optional[str]
    subtitle: Optional[str]
    genres: List[str]
    publishedYear: Optional[str]
    publishedDate: Optional[str]
    publisher: Optional[str]
    description: Optional[str]
    isbn: Optional[str]
    asin: Optional[str]
    language: Optional[str]
    explicit: bool



@dataclass
class BookMetadataExpanded(Base):
    """
    Represents expanded metadata for a book.

    Attributes:
        title (str or None): The title of the book. Will be None if unknown.
        subtitle (str or None): The subtitle of the book. Will be None if there is no subtitle.
        authors (List[AuthorMinified]): The authors of the book.
        narrators (List[str]): The narrators of the audiobook.
        series (List[SeriesSequence]): The series the book belongs to.
        genres (List[str]): The genres of the book.
        publishedYear (str or None): The year the book was published. Will be null if unknown.
        publishedDate (str or None): The date the book was published. Will be null if unknown.
        publisher (str or None): The publisher of the book. Will be null if unknown.
        description (str or None): A description for the book. Will be null if empty.
        isbn (str or None): The ISBN of the book. Will be null if unknown.
        asin (str or None): The ASIN of the book. Will be null if unknown.
        language (str or None): The language of the book. Will be null if unknown.
        explicit (bool): Whether the book has been marked as explicit.
        titleIgnorePrefix (str): The title of the book with any prefix moved to the end.
        authorName (str): The name of the book's author(s).
        authorNameLF (str): The name of the book's author(s) with last names first.
        narratorName (str): The name of the audiobook's narrator(s).
        seriesName (str): The name of the book's series.
    """
    title: str
    subtitle: str
    authors: List[AuthorMinified]
    narrators: List[str]
    series: List[Type['SeriesSequence']]
    genres: List[str]
    publishedYear: str
    publishedDate: str
    publisher: str
    description: str
    isbn: str
    asin: str
    language: str
    explicit: bool
    titleIgnorePrefix: str
    authorName: str
    authorNameLF: str
    narratorName: str
    seriesName: str


#BookMetadata, AudioFIle, BookChapter, EBookFile
@dataclass
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
  audioFiles: List[Type['AudioFile']]
  chapters: List[Type['BookChapter']]
  missingParts: List[int]
  ebookFile: Optional[Type['EBookFile']]


@dataclass
class BookMinified(Base):
    """
    Represents a minified book.

    Attributes:
        metadata (BookMetadataMinified): The book's metadata.
        coverPath (str or None): The absolute path on the server of the cover file. Will be None if there is no cover.
        numTracks (int): The number of tracks the book's audio files have.
        numAudioFiles (int): The number of audio files the book has.
        numChapters (int): The number of chapters the book has.
        numMissingParts (int): The total number of missing parts the book has.
        numInvalidAudioFiles (int): The number of invalid audio files the book has.
        duration (float): The total length (in seconds) of the book.
        size (int): The total size (in bytes) of the book.
        ebookFormat (str or None): The format of the ebook of the book. Will be None if the book is an audiobook.
    """
    metadata: BookMetadataMinified
    coverPath: Optional[str]
    numTracks: int
    numAudioFiles: int
    numChapters: int
    numMissingParts: int
    numInvalidAudioFiles: int
    duration: float
    size: int
    ebookFormat: Optional[str]


@dataclass
class BookExpanded(Base):
    """
    Represents an expanded book.

    Attributes:
        libraryItemId (str): The ID of the library item that contains the book.
        metadata (BookMetadataExpanded): The book's expanded metadata.
        coverPath (str or None): The absolute path on the server of the cover file. Will be None if there is no cover.
        tags (List[str]): The book's tags.
        audioFiles (List[AudioFile]): The book's audio files.
        chapters (List[BookChapter]): The book's chapters.
        missingParts (List[int]): Any parts missing from the book by track index.
        ebookFile (Optional[EBookFile]): The book's ebook file. Will be None if this is an audiobook.
        duration (float): The total length (in seconds) of the book.
        size (int): The total size (in bytes) of the book.
        tracks (List[AudioTrack]): The book's audio tracks from the audio files.
    """
    libraryItemId: str
    metadata: BookMetadataExpanded
    coverPath: Optional[str]
    tags: List[str]
    audioFiles: List[AudioFile]
    chapters: List[BookChapter]
    missingParts: List[int]
    ebookFile: Optional[EBookFile]
    duration: float
    size: int
    tracks: List[AudioTrack]


@dataclass
class LibraryItem(Base):
    """
    Represents a library item.

    Attributes:
        id (str): The ID of the library item.
        ino (str): The inode of the library item.
        libraryId (str): The ID of the library the item belongs to.
        folderId (str): The ID of the folder the library item is in.
        path (str): The path of the library item on the server.
        relPath (str): The path, relative to the library folder, of the library item.
        isFile (bool): Whether the library item is a single file in the root of the library folder.
        mtimeMs (int): The time (in ms since POSIX epoch) when the library item was last modified on disk.
        ctimeMs (int): The time (in ms since POSIX epoch) when the library item status was changed on disk.
        birthtimeMs (int): The time (in ms since POSIX epoch) when the library item was created on disk. Will be 0 if unknown.
        addedAt (int): The time (in ms since POSIX epoch) when the library item was added to the library.
        updatedAt (int): The time (in ms since POSIX epoch) when the library item was last updated. (Read Only)
        lastScan (int or None): The time (in ms since POSIX epoch) when the library item was last scanned. Will be None if the server has not yet scanned the library item.
        scanVersion (str or None): The version of the scanner when last scanned. Will be null if it has not been scanned.
        isMissing (bool): Whether the library item was scanned and no longer exists.
        isInvalid (bool): Whether the library item was scanned and no longer has media files.
        mediaType (str): What kind of media the library item contains. Will be book or podcast.
        media: Union[Book, Podcast]: The media of the library item.
        libraryFiles (List[LibraryFile]): The files of the library item.
    """
    id: str
    ino: str
    libraryId: str
    folderId: str
    path: str
    relPath: str
    isFile: bool
    mtimeMs: int
    ctimeMs: int
    birthtimeMs: int
    addedAt: int
    updatedAt: int
    lastScan: Optional[int]
    scanVersion: Optional[str]
    isMissing: bool
    isInvalid: bool
    mediaType: str
    media: Union[Book, Podcast]
    libraryFiles: List[LibraryFile]


@dataclass
class Series(Base):
    """
    Represents a series.

    Attributes:
        id (str): The ID of the series.
        name (str): The name of the series.
        description (str or None): A description for the series. Will be None if there is none.
        addedAt (int): The time (in ms since POSIX epoch) when the series was added.
        updatedAt (int): The time (in ms since POSIX epoch) when the series was last updated.
    """
    id: str
    name: str
    description: Optional[str]
    addedAt: int
    updatedAt: int


@dataclass
class SeriesNumBooks(Base):
    """
    Represents a series with the number of books.

    Attributes:
        id (str): The ID of the series.
        name (str): The name of the series.
        nameIgnorePrefix (str): The name of the series with any prefix moved to the end.
        libraryItemIds (List[str]): The IDs of the library items in the series.
        numBooks (int): The number of books in the series.
    """
    id: str
    name: str
    nameIgnorePrefix: str
    libraryItemIds: List[str]
    numBooks: int


@dataclass
class SeriesBooks(Base):
    """
    Represents a series with updated attributes.

    Attributes:
        id (str): The ID of the series.
        name (str): The name of the series.
        nameIgnorePrefix (str): The name of the series with any prefix moved to the end.
        nameIgnorePrefixSort (str): The name of the series with any prefix removed.
        type (str): Will always be series.
        books (List[LibraryItem]): The library items that contain the books in the series.
            A sequence attribute that denotes the position in the series the book is in, is tacked on.
        totalDuration (float): The combined duration (in seconds) of all books in the series.
    """
    id: str
    name: str
    nameIgnorePrefix: str
    nameIgnorePrefixSort: str
    type: str
    books: List[LibraryItem]
    totalDuration: float


@dataclass
class SeriesSequence(Base):
    """
    Represents a series with updated attributes.

    Attributes:
        id (str): The ID of the series.
        name (str): The name of the series.
        sequence (str or None): The position in the series the book is. Will be None if unknown.
    """
    id: str
    name: str
    sequence: Optional[str]


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

  
@dataclass
class LibraryFilterData(Base):
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
  languages: List[str]


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


