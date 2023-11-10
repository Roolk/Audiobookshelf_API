import typing
from dataclasses import dataclass, asdict, fields
from typing import Optional, List, Union, Type

__all__ = ['AudioFile', 'AudioMetaTags', 'AudioTrack', 'Author', 'AuthorExpanded', 'AuthorMinified', 'Book',
           'BookExpanded', 'BookMinified', 'BookMetadata', 'BookMetadataExpanded', 'BookMetadataMinified', 'EBookFile',
           'FileMetadata', 'Folder', 'Library', 'LibraryFile', 'LibraryFilterData', 'LibraryItem', 'LibrarySettings',
           'Podcast', 'PodcastExpanded', 'PodcastMinified', 'PodcastEpisode', 'PodcastEpisodeExpanded',
           'PodcastEpisodeDownload', 'PodcastEpisodeEnclosure', 'PodcastMetadata', 'PodcastMetadataExpanded',
           'PodcastMetadataMinified', 'Series', 'SeriesBooks', 'SeriesNumBooks', 'SeriesSequence']


@dataclass
class Base:
    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        """
        Create a class instance from a dictionary.

        This method constructs a class instance by mapping keys in a dictionary
        to attributes of the class. It automatically converts nested dictionaries
        into instances of their respective classes.

        Args:
            cls (Type[Base]): The class type to instantiate.
            data (dict): The dictionary containing data to populate the instance.

        Returns:
            Base: An instance of the class with attributes populated from the dictionary.

        Note:
            This method may not work for unions. If you need to handle unions,
            consider using `__postinit__` methods to convert to specific types.
        """
        valid_data = {field.name: data[field.name] if field.name in data else None for field in fields(cls)}

        new_instance = cls(**valid_data)

        for field in fields(new_instance):
            new_instance._convert_field_to_class(field)

        return new_instance

    def _convert_field_to_class(self, field):
        # this does not work for unions, therefore __postinit__ are required to
        # convert the unions to a specific type

        # if the class to convert to is specified use that, useful for unions

        if (isinstance(field.type, Base)):
            # converts dict into class
            setattr(self, field.type, field.type.from_dict(getattr(self, field.name)))

        elif isinstance(field.type, List) and hasattr(field.type, '__args__') and len(
            field.type.__args__) > 0 and isinstance(field.type.__args__[0], Base):
            # converts the list of dicts to a list of classes
            converted_list = [field.type.__args__[0].from_dict(item)
                              for item in getattr(self, field.name)]
            setattr(self, field.name, converted_list)


@dataclass
class AudioFile(Base):
    """
    Represents an audio file.

    Attributes:
        index (int): The index of the audio file.
        ino (str): The inode of the audio file.
        metadata (FileMetadata): The audio file's metadata.
        addedAt (int): The time (in ms since POSIX epoch) when the audio file was added to the library.
        updatedAt (int): The time (in ms since POSIX epoch) when the audio file last updated. (Read Only)
        trackNumFromMeta (int or None): The track number of the audio file as pulled from the file's metadata. Will be null if unknown.
        discNumFromMeta (int or None): The disc number of the audio file as pulled from the file's metadata. Will be null if unknown.
        trackNumFromFilename (int or None): The track number of the audio file as determined from the file's name. Will be null if unknown.
        discNumFromFilename (int or None): The track number of the audio file as determined from the file's name. Will be null if unknown.
        manuallyVerified (bool): Whether the audio file has been manually verified by a user.
        invalid (bool): Whether the audio file is missing from the server.
        exclude (bool): Whether the audio file has been marked for exclusion.
        error (str or None): Any error with the audio file. Will be null if there is none.
        format (str): The format of the audio file.
        duration (float): The total length (in seconds) of the audio file.
        bitRate (int): The bit rate (in bit/s) of the audio file.
        language (str or None): The language of the audio file.
        codec (str): The codec of the audio file.
        timeBase (str): The time base of the audio file.
        channels (int): The number of channels the audio file has.
        channelLayout (str): The layout of the audio file's channels.
        chapters (List[BookChapter]): If the audio file is part of an audiobook, the chapters the file contains.
        embeddedCoverArt (str or None): The type of embedded cover art in the audio file. Will be null if none exists.
        metaTags (AudioMetaTags): The audio metadata tags from the audio file.
        mimeType (str): The MIME type of the audio file.
    """
    index: int
    ino: str
    metadata: Type['FileMetadata']
    addedAt: int
    updatedAt: int
    trackNumFromMeta: Optional[int]
    discNumFromMeta: Optional[int]
    trackNumFromFilename: Optional[int]
    discNumFromFilename: Optional[int]
    manuallyVerified: bool
    invalid: bool
    exclude: bool
    error: Optional[str]
    format: str
    duration: float
    bitRate: int
    language: Optional[str]
    codec: str
    timeBase: str
    channels: int
    channelLayout: str
    chapters: List[Type['BookChapter']]
    embeddedCoverArt: Optional[str]
    metaTags: Type['AudioMetaTags']
    mimeType: str


@dataclass
class AudioMetaTags(Base):
    """
    Represents ID3 metadata tags pulled from the audio file on import.

    Attributes:
        tagAlbum (str or None): The album name tag from the audio file.
        tagArtist (str or None): The artist name tag from the audio file.
        tagGenre (str or None): The genre tag from the audio file.
        tagTitle (str or None): The title tag from the audio file.
        tagSeries (str or None): The series name tag from the audio file.
        tagSeriesPart (str or None): The series part tag from the audio file.
        tagTrack (str or None): The track number tag from the audio file.
        tagDisc (str or None): The disc number tag from the audio file.
        tagSubtitle (str or None): The subtitle tag from the audio file.
        tagAlbumArtist (str or None): The album artist tag from the audio file.
        tagDate (str or None): The date tag from the audio file.
        tagComposer (str or None): The composer tag from the audio file.
        tagPublisher (str or None): The publisher tag from the audio file.
        tagComment (str or None): The comment tag from the audio file.
        tagDescription (str or None): The description tag from the audio file.
        tagEncoder (str or None): The encoder tag from the audio file.
        tagEncodedBy (str or None): The encoded by tag from the audio file.
        tagIsbn (str or None): The ISBN tag from the audio file.
        tagLanguage (str or None): The language tag from the audio file.
        tagASIN (str or None): The ASIN tag from the audio file.
        tagOverdriveMediaMarker (str or None): The Overdrive Media Marker tag from the audio file.
        tagOriginalYear (str or None): The original year tag from the audio file.
        tagReleaseCountry (str or None): The release country tag from the audio file.
        tagReleaseType (str or None): The release type tag from the audio file.
        tagReleaseStatus (str or None): The release status tag from the audio file.
        tagISRC (str or None): The ISRC tag from the audio file.
        tagMusicBrainzTrackId (str or None): The MusicBrainz Track ID tag from the audio file.
        tagMusicBrainzAlbumId (str or None): The MusicBrainz Album ID tag from the audio file.
        tagMusicBrainzAlbumArtistId (str or None): The MusicBrainz Album Artist ID tag from the audio file.
        tagMusicBrainzArtistId (str or None): The MusicBrainz Artist ID tag from the audio file.
    """
    tagAlbum: Optional[str]
    tagArtist: Optional[str]
    tagGenre: Optional[str]
    tagTitle: Optional[str]
    tagSeries: Optional[str]
    tagSeriesPart: Optional[str]
    tagTrack: Optional[str]
    tagDisc: Optional[str]
    tagSubtitle: Optional[str]
    tagAlbumArtist: Optional[str]
    tagDate: Optional[str]
    tagComposer: Optional[str]
    tagPublisher: Optional[str]
    tagComment: Optional[str]
    tagDescription: Optional[str]
    tagEncoder: Optional[str]
    tagEncodedBy: Optional[str]
    tagIsbn: Optional[str]
    tagLanguage: Optional[str]
    tagASIN: Optional[str]
    tagOverdriveMediaMarker: Optional[str]
    tagOriginalYear: Optional[str]
    tagReleaseCountry: Optional[str]
    tagReleaseType: Optional[str]
    tagReleaseStatus: Optional[str]
    tagISRC: Optional[str]
    tagMusicBrainzTrackId: Optional[str]
    tagMusicBrainzAlbumId: Optional[str]
    tagMusicBrainzAlbumArtistId: Optional[str]
    tagMusicBrainzArtistId: Optional[str]


@dataclass
class AudioTrack(Base):
    """
    Represents an audio track.

    Attributes:
        index (int): The index of the audio track.
        startOffset (float): When in the audio file (in seconds) the track starts.
        duration (float): The length (in seconds) of the audio track.
        title (str): The filename of the audio file the audio track belongs to.
        contentUrl (str): The URL path of the audio file.
        mimeType (str): The MIME type of the audio file.
        metadata (FileMetadata or None): The metadata of the audio file. Will be null if there is none.
    """
    index: int
    startOffset: float
    duration: float
    title: str
    contentUrl: str
    mimeType: str
    metadata: Optional[Type['FileMetadata']]


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
    metadata: Type['BookMetadata']
    coverPath: Optional[str]
    tags: List[str]
    audioFiles: List[Type['AudioFile']]
    chapters: List[Type['BookChapter']]
    missingParts: List[int]
    ebookFile: Optional[Type['EBookFile']]


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
    metadata: Type['BookMetadataExpanded']
    coverPath: Optional[str]
    tags: List[str]
    audioFiles: List[Type['AudioFile']]
    chapters: List[Type['BookChapter']]
    missingParts: List[int]
    ebookFile: Optional[Type['EBookFile']]
    duration: float
    size: int
    tracks: List[Type['AudioTrack']]


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
    metadata: Type['BookMetadataMinified']
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
class BookChapter(Base):
    """
    Represents a chapter in a book.

    Attributes:
        id (int): The ID of the book chapter.
        start (float): When in the book (in seconds) the chapter starts.
        end (float): When in the book (in seconds) the chapter ends.
        title (str): The title of the chapter.
    """
    id: int
    start: float
    end: float
    title: str


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
class Collection(Base):
    """
    Represents a collection.

    Attributes:
        id (str): The ID of the collection.
        libraryId (str): The ID of the library the collection belongs to.
        userId (str): The ID of the user that created the collection.
        name (str): The name of the collection.
        description (str or None): The collection's description. Will be None if there is none.
        books (List[LibraryItem]): The books that belong to the collection.
        lastUpdate (int): The time (in ms since POSIX epoch) when the collection was last updated.
        createdAt (int): The time (in ms since POSIX epoch) when the collection was created.
    """
    id: str
    libraryId: str
    userId: str
    name: str
    description: Optional[str]
    books: List[Type['LibraryItem']]
    lastUpdate: int
    createdAt: int



@dataclass
class CollectionExpanded(Base):
    """
    Represents a collection.

    Attributes:
        id (str): The ID of the collection.
        libraryId (str): The ID of the library the collection belongs to.
        userId (str): The ID of the user that created the collection.
        name (str): The name of the collection.
        description (str or None): The collection's description. Will be None if there is none.
        books (List[LibraryItemExpanded]): The books that belong to the collection.
        lastUpdate (int): The time (in ms since POSIX epoch) when the collection was last updated.
        createdAt (int): The time (in ms since POSIX epoch) when the collection was created.
    """
    id: str
    libraryId: str
    userId: str
    name: str
    description: Optional[str]
    books: List[Type['LibraryItemExpanded']]
    lastUpdate: int
    createdAt: int


@dataclass
class EBookFile(Base):
    """
    Represents an ebook file.

    Attributes:
        ino (str): The inode of the ebook file.
        metadata (FileMetadata): The metadata of the ebook file.
        ebookFormat (str): The ebook format of the ebook file.
        addedAt (int): The time (in ms since POSIX epoch) when the ebook file was added.
        updatedAt (int): The time (in ms since POSIX epoch) when the ebook file was last updated.
    """
    ino: str
    metadata: Type['FileMetadata']
    ebookFormat: str
    addedAt: int
    updatedAt: int


@dataclass
class FileMetadata(Base):
    """
    Represents metadata for a file.

    Attributes:
        filename (str): The filename of the file.
        ext (str): The file extension of the file.
        path (str): The absolute path on the server of the file.
        relPath (str): The path of the file, relative to the book's or podcast's folder.
        size (int): The size (in bytes) of the file.
        mtimeMs (int): The time (in ms since POSIX epoch) when the file was last modified on disk.
        ctimeMs (int): The time (in ms since POSIX epoch) when the file status was changed on disk.
        birthtimeMs (int): The time (in ms since POSIX epoch) when the file was created on disk. Will be 0 if unknown.
    """
    filename: str
    ext: str
    path: str
    relPath: str
    size: int
    mtimeMs: int
    ctimeMs: int
    birthtimeMs: int


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
class LibraryFile(Base):
    """
    Represents a library file.

    Attributes:
        ino (str): The inode of the library file.
        metadata (FileMetadata): The metadata for the library file.
        addedAt (int): The time (in ms since POSIX epoch) when the library file was added.
        updatedAt (int): The time (in ms since POSIX epoch) when the library file was last updated.
        fileType (str): The type of file that the library file is (audio, image, etc.).
    """
    ino: str
    metadata: Type['FileMetadata']
    addedAt: int
    updatedAt: int
    fileType: str


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
    series: List[Type['Series']]
    narrators: List[str]
    languages: List[str]


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
        libraryFiles (List[LibraryFile] or None): The files of the library item.

    Notes:
        libraryFiles is not defined as optional in the audiobookshelf api but get_all_library_items does not return the
        libraryFiles array
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
    media: Union[Type['Book'], Type['Podcast']]
    libraryFiles: Optional[List[Type['LibraryFile']]]

    def __post_init__(self):
        # updates the media attribute from a dict to Book or Podcast
        if type(self.media) is dict:
            if self.mediaType == 'book':
                self.media = Book.from_dict(self.media)
            else:
                self.media = Podcast.from_dict(self.media)



@dataclass
class LibraryItemExpanded(Base):
    """
    Represents an expanded version of a library item.

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
        birthtimeMs (int): The time (in ms since POSIX epoch) when the library item was created on disk.
            Will be 0 if unknown.
        addedAt (int): The time (in ms since POSIX epoch) when the library item was added to the library.
        updatedAt (int): The time (in ms since POSIX epoch) when the library item was last updated.
        lastScan (int or None): The time (in ms since POSIX epoch) when the library item was last scanned.
            Will be None if the server has not yet scanned the library item.
        scanVersion (str or None): The version of the scanner when last scanned.
            Will be None if it has not been scanned.
        isMissing (bool): Whether the library item was scanned and no longer exists.
        isInvalid (bool): Whether the library item was scanned and no longer has media files.
        mediaType (str): What kind of media the library item contains. Will be book or podcast.
        media (BookExpanded or PodcastExpanded): The expanded media object of the library item.
        libraryFiles (List[LibraryFile]): The files of the library item.
        size (int): The total size (in bytes) of the library item.
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
    media: Union[Type['BookExpanded'], Type['PodcastExpanded']]
    libraryFiles: List[LibraryFile]
    size: int

    def __post_init__(self):
        # updates the media attribute from a dict to Book or Podcast
        if type(self.media) is dict:
            if self.mediaType == 'book':
                self.media = BookExpanded.from_dict(self.media)
            else:
                self.media = PodcastExpanded.from_dict(self.media)

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
class Podcast(Base):
    """
    Represents a podcast.

    Attributes:
        libraryItemId (str): The ID of the library item that contains the podcast.
        metadata (PodcastMetadata): The metadata for the podcast.
        coverPath (str or None): The absolute path on the server of the cover file. Will be None if there is no cover.
        tags (List[str]): The podcast's tags.
        episodes (List[PodcastEpisode]): The downloaded episodes of the podcast.
        autoDownloadEpisodes (bool): Whether the server will automatically download podcast episodes according to the schedule.
        autoDownloadSchedule (str or None): The cron expression for when to automatically download podcast episodes.
            Will not exist if autoDownloadEpisodes is false.
        lastEpisodeCheck (int): The time (in ms since POSIX epoch) when the podcast was checked for new episodes.
        maxEpisodesToKeep (int): The maximum number of podcast episodes to keep when automatically downloading new episodes.
            Episodes beyond this limit will be deleted. If 0, all episodes will be kept.
        maxNewEpisodesToDownload (int): The maximum number of podcast episodes to download when automatically downloading new episodes.
            If 0, all episodes will be downloaded.
    """
    libraryItemId: str
    metadata: Type['PodcastMetadata']
    coverPath: Optional[str]
    tags: List[str]
    episodes: List[Type['PodcastEpisode']]
    autoDownloadEpisodes: bool
    autoDownloadSchedule: Optional[str]
    lastEpisodeCheck: int
    maxEpisodesToKeep: int
    maxNewEpisodesToDownload: int


@dataclass
class PodcastExpanded(Base):
    """
    Represents an expanded version of a podcast.

    Attributes:
        libraryItemId (str): The ID of the library item that contains the podcast.
        metadata (PodcastMetadataExpanded): The metadata for the podcast.
        coverPath (str or None): The absolute path on the server of the cover file. Will be None if there is no cover.
        tags (List[str]): The podcast's tags.
        episodes (List[PodcastEpisodeExpanded]): The downloaded episodes of the podcast.
        autoDownloadEpisodes (bool): Whether the server will automatically download podcast episodes according to the schedule.
        autoDownloadSchedule (str or None): The cron expression for when to automatically download podcast episodes.
            Will not exist if autoDownloadEpisodes is false.
        lastEpisodeCheck (int): The time (in ms since POSIX epoch) when the podcast was checked for new episodes.
        maxEpisodesToKeep (int): The maximum number of podcast episodes to keep when automatically downloading new episodes.
            Episodes beyond this limit will be deleted. If 0, all episodes will be kept.
        maxNewEpisodesToDownload (int): The maximum number of podcast episodes to download when automatically downloading new episodes.
            If 0, all episodes will be downloaded.
        size (int): The total size (in bytes) of the podcast.
    """
    libraryItemId: str
    metadata: Type['PodcastMetadataExpanded']
    coverPath: Optional[str]
    tags: List[str]
    episodes: List[Type['PodcastEpisodeExpanded']]
    autoDownloadEpisodes: bool
    autoDownloadSchedule: Optional[str]
    lastEpisodeCheck: int
    maxEpisodesToKeep: int
    maxNewEpisodesToDownload: int
    size: int


@dataclass
class PodcastMinified(Base):
    """
    Represents a minified version of a podcast.

    Attributes:
        metadata (PodcastMetadataMinified): The metadata for the podcast.
        coverPath (str or None): The absolute path on the server of the cover file. Will be None if there is no cover.
        tags (List[str]): The podcast's tags.
        autoDownloadEpisodes (bool): Whether the server will automatically download podcast episodes according to the schedule.
        autoDownloadSchedule (str or None): The cron expression for when to automatically download podcast episodes.
            Will not exist if autoDownloadEpisodes is false.
        lastEpisodeCheck (int): The time (in ms since POSIX epoch) when the podcast was checked for new episodes.
        maxEpisodesToKeep (int): The maximum number of podcast episodes to keep when automatically downloading new episodes.
            Episodes beyond this limit will be deleted. If 0, all episodes will be kept.
        maxNewEpisodesToDownload (int): The maximum number of podcast episodes to download when automatically downloading new episodes.
            If 0, all episodes will be downloaded.
        numEpisodes (int): The number of downloaded episodes for the podcast.
        size (int): The total size (in bytes) of the podcast.
    """
    metadata: Type['PodcastMetadataMinified']
    coverPath: Optional[str]
    tags: List[str]
    autoDownloadEpisodes: bool
    autoDownloadSchedule: Optional[str]
    lastEpisodeCheck: int
    maxEpisodesToKeep: int
    maxNewEpisodesToDownload: int
    numEpisodes: int
    size: int


@dataclass
class PodcastEpisode(Base):
    """
    Represents a podcast episode.

    Attributes:
        libraryItemId (str): The ID of the library item that contains the podcast.
        id (str): The ID of the podcast episode.
        index (int): The index of the podcast episode.
        season (str or None): The season of the podcast episode, if known.
        episode (str or None): The episode of the season of the podcast, if known.
        episodeType (str): The type of episode that the podcast episode is.
        title (str): The title of the podcast episode.
        subtitle (str or None): The subtitle of the podcast episode.
        description (str): A HTML encoded, description of the podcast episode.
        enclosure (PodcastEpisodeEnclosure): Information about the podcast episode from when it was downloaded.
        pubDate (str): When the podcast episode was published.
        audioFile (AudioFile): The audio file for the podcast episode.
        publishedAt (int): The time (in ms since POSIX epoch) when the podcast episode was published.
        addedAt (int): The time (in ms since POSIX epoch) when the podcast episode was added to the library.
        updatedAt (int): The time (in ms since POSIX epoch) when the podcast episode was last updated.
    """
    libraryItemId: str
    id: str
    index: int
    season: Optional[str]
    episode: Optional[str]
    episodeType: str
    title: str
    subtitle: Optional[str]
    description: str
    enclosure: Type['PodcastEpisodeEnclosure']
    pubDate: str
    audioFile: AudioFile
    publishedAt: int
    addedAt: int
    updatedAt: int


@dataclass
class PodcastEpisodeExpanded(Base):
    """
    Represents a podcast episode.

    Attributes:
        libraryItemId (str): The ID of the library item that contains the podcast.
        id (str): The ID of the podcast episode.
        index (int): The index of the podcast episode.
        season (str or None): The season of the podcast episode, if known.
        episode (str or None): The episode of the season of the podcast, if known.
        episodeType (str): The type of episode that the podcast episode is.
        title (str): The title of the podcast episode.
        subtitle (str or None): The subtitle of the podcast episode.
        description (str): A HTML encoded, description of the podcast episode.
        enclosure (PodcastEpisodeEnclosure): Information about the podcast episode from when it was downloaded.
        pubDate (str): When the podcast episode was published.
        audioFile (AudioFile): The audio file for the podcast episode.
        publishedAt (int): The time (in ms since POSIX epoch) when the podcast episode was published.
        addedAt (int): The time (in ms since POSIX epoch) when the podcast episode was added to the library.
        updatedAt (int): The time (in ms since POSIX epoch) when the podcast episode was last updated.
        audioTrack (AudioTrack): The podcast episode's audio tracks from the audio file.
        duration (float): The total length (in seconds) of the podcast episode.
        size (int): The total size (in bytes) of the podcast episode.
    """
    libraryItemId: str
    id: str
    index: int
    season: Optional[str]
    episode: Optional[str]
    episodeType: str
    title: str
    subtitle: Optional[str]
    description: str
    enclosure: Type['PodcastEpisodeEnclosure']
    pubDate: str
    audioFile: AudioFile
    publishedAt: int
    addedAt: int
    updatedAt: int
    audioTrack: Type['AudioTrack']
    duration: float
    size: int


@dataclass
class PodcastEpisodeDownload(Base):
    """
    Represents a podcast episode download.

    Attributes:
        id (str): The ID of the podcast episode download.
        episodeDisplayTitle (str): The display title of the episode to be downloaded.
        url (str): The URL from which to download the episode.
        libraryItemId (str): The ID of the library item the episode belongs to.
        libraryId (str): The ID of the library the episode's podcast belongs to.
        isFinished (bool): Whether the episode has finished downloading.
        failed (bool): Whether the episode failed to download.
        startedAt (int or None): The time (in ms since POSIX epoch) when the episode started downloading.
        createdAt (int): The time (in ms since POSIX epoch) when the podcast episode download request was created.
        finishedAt (int or None): The time (in ms since POSIX epoch) when the episode finished downloading.
        podcastTitle (str or None): The title of the episode's podcast.
        podcastExplicit (bool): Whether the episode's podcast is explicit.
        season (str or None): The season of the podcast episode.
        episode (str or None): The episode number of the podcast episode.
        episodeType (str): The type of the podcast episode.
        publishedAt (int or None): The time (in ms since POSIX epoch) when the episode was published.
    """
    id: str
    episodeDisplayTitle: str
    url: str
    libraryItemId: str
    libraryId: str
    isFinished: bool
    failed: bool
    startedAt: Optional[int]
    createdAt: int
    finishedAt: Optional[int]
    podcastTitle: Optional[str]
    podcastExplicit: bool
    season: Optional[str]
    episode: Optional[str]
    episodeType: str
    publishedAt: Optional[int]


@dataclass
class PodcastEpisodeEnclosure(Base):
    """
    Represents the enclosure information for a podcast episode.

    Attributes:
        url (str): The URL where the podcast episode's audio file was downloaded from.
        type (str): The MIME type of the podcast episode's audio file.
        length (str): The size (in bytes) that was reported when downloading the podcast episode's audio file.
    """
    url: str
    type: str
    length: str


@dataclass
class PodcastMetadata(Base):
    """
    Represents the metadata for a podcast.

    Attributes:
        title (str or None): The title of the podcast. Will be None if unknown.
        author (str or None): The author of the podcast. Will be None if unknown.
        description (str or None): The description for the podcast. Will be None if unknown.
        releaseDate (str or None): The release date of the podcast. Will be None if unknown.
        genres (List[str]): The podcast's genres.
        feedUrl (str or None): A URL of an RSS feed for the podcast. Will be None if unknown.
        imageUrl (str or None): A URL of a cover image for the podcast. Will be None if unknown.
        itunesPageUrl (str or None): A URL of an iTunes page for the podcast. Will be None if unknown.
        itunesId (int or None): The iTunes ID for the podcast. Will be None if unknown.
        itunesArtistId (int or None): The iTunes Artist ID for the author of the podcast. Will be None if unknown.
        explicit (bool): Whether the podcast has been marked as explicit.
        language (str or None): The language of the podcast. Will be None if unknown.
        type (str or None): The type of podcast. Will be None if unknown.
    """
    title: Optional[str]
    author: Optional[str]
    description: Optional[str]
    releaseDate: Optional[str]
    genres: List[str]
    feedUrl: Optional[str]
    imageUrl: Optional[str]
    itunesPageUrl: Optional[str]
    itunesId: Optional[int]
    itunesArtistId: Optional[int]
    explicit: bool
    language: Optional[str]
    type: Optional[str]


@dataclass
class PodcastMetadataExpanded(Base):
    """
    Represents the metadata for a podcast.

    Attributes:
        title (str or None): The title of the podcast. Will be None if unknown.
        titleIgnorePrefix (str): The title of the podcast with any prefix moved to the end.
        author (str or None): The author of the podcast. Will be None if unknown.
        description (str or None): The description for the podcast. Will be None if unknown.
        releaseDate (str or None): The release date of the podcast. Will be None if unknown.
        genres (List[str]): The podcast's genres.
        feedUrl (str or None): A URL of an RSS feed for the podcast. Will be None if unknown.
        imageUrl (str or None): A URL of a cover image for the podcast. Will be None if unknown.
        itunesPageUrl (str or None): A URL of an iTunes page for the podcast. Will be None if unknown.
        itunesId (int or None): The iTunes ID for the podcast. Will be None if unknown.
        itunesArtistId (int or None): The iTunes Artist ID for the author of the podcast. Will be None if unknown.
        explicit (bool): Whether the podcast has been marked as explicit.
        language (str or None): The language of the podcast. Will be None if unknown.
        type (str or None): The type of podcast. Will be None if unknown.
    """
    title: Optional[str]
    titleIgnorePrefix: str
    author: Optional[str]
    description: Optional[str]
    releaseDate: Optional[str]
    genres: List[str]
    feedUrl: Optional[str]
    imageUrl: Optional[str]
    itunesPageUrl: Optional[str]
    itunesId: Optional[int]
    itunesArtistId: Optional[int]
    explicit: bool
    language: Optional[str]
    type: Optional[str]


@dataclass
class PodcastMetadataMinified(Base):
    """
    Represents the metadata for a podcast.

    Attributes:
        title (str or None): The title of the podcast. Will be None if unknown.
        titleIgnorePrefix (str): The title of the podcast with any prefix moved to the end.
        author (str or None): The author of the podcast. Will be None if unknown.
        description (str or None): The description for the podcast. Will be None if unknown.
        releaseDate (str or None): The release date of the podcast. Will be None if unknown.
        genres (List[str]): The podcast's genres.
        feedUrl (str or None): A URL of an RSS feed for the podcast. Will be None if unknown.
        imageUrl (str or None): A URL of a cover image for the podcast. Will be None if unknown.
        itunesPageUrl (str or None): A URL of an iTunes page for the podcast. Will be None if unknown.
        itunesId (int or None): The iTunes ID for the podcast. Will be None if unknown.
        itunesArtistId (int or None): The iTunes Artist ID for the author of the podcast. Will be None if unknown.
        explicit (bool): Whether the podcast has been marked as explicit.
        language (str or None): The language of the podcast. Will be None if unknown.
        type (str or None): The type of podcast. Will be None if unknown.
    """
    title: Optional[str]
    titleIgnorePrefix: str
    author: Optional[str]
    description: Optional[str]
    releaseDate: Optional[str]
    genres: List[str]
    feedUrl: Optional[str]
    imageUrl: Optional[str]
    itunesPageUrl: Optional[str]
    itunesId: Optional[int]
    itunesArtistId: Optional[int]
    explicit: bool
    language: Optional[str]
    type: Optional[str]


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
