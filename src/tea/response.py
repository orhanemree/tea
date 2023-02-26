from typing import Union
from datetime import datetime
from pathlib import Path

status_list = {
    "202": "ACCEPTED",
    "208": "ALREADY REPORTED",
    "502": "BAD GATEWAY",
    "400": "BAD REQUEST",
    "409": "CONFLICT",
    "100": "CONTINUE",
    "201": "CREATED",
    "103": "EARLY HINTS",
    "417": "EXPECTATION FAILED",
    "424": "FAILED DEPENDENCY",
    "403": "FORBIDDEN",
    "302": "FOUND",
    "504": "GATEWAY TIMEOUT",
    "410": "GONE",
    "505": "HTTP VERSION NOT SUPPORTED",
    "418": "IM A TEAPOT",
    "226": "IM USED",
    "507": "INSUFFICIENT STORAGE",
    "500": "INTERNAL SERVER ERROR",
    "411": "LENGTH REQUIRED",
    "423": "LOCKED",
    "508": "LOOP DETECTED",
    "405": "METHOD NOT ALLOWED",
    "421": "MISDIRECTED REQUEST",
    "301": "MOVED PERMANENTLY",
    "300": "MULTIPLE CHOICES",
    "207": "MULTI STATUS",
    "511": "NETWORK AUTHENTICATION REQUIRED",
    "203": "NON AUTHORITATIVE INFORMATION",
    "406": "NOT ACCEPTABLE",
    "510": "NOT EXTENDED",
    "404": "NOT FOUND",
    "501": "NOT IMPLEMENTED",
    "304": "NOT MODIFIED",
    "204": "NO CONTENT",
    "200": "OK",
    "206": "PARTIAL CONTENT",
    "402": "PAYMENT REQUIRED",
    "308": "PERMANENT REDIRECT",
    "412": "PRECONDITION FAILED",
    "428": "PRECONDITION REQUIRED",
    "102": "PROCESSING",
    "407": "PROXY AUTHENTICATION REQUIRED",
    "416": "REQUESTED RANGE NOT SATISFIABLE",
    "413": "REQUEST ENTITY TOO LARGE",
    "431": "REQUEST HEADER FIELDS TOO LARGE",
    "408": "REQUEST TIMEOUT",
    "414": "REQUEST URI TOO LONG",
    "205": "RESET CONTENT",
    "303": "SEE OTHER",
    "503": "SERVICE UNAVAILABLE",
    "101": "SWITCHING PROTOCOLS",
    "307": "TEMPORARY REDIRECT",
    "425": "TOO EARLY",
    "429": "TOO MANY REQUESTS",
    "401": "UNAUTHORIZED",
    "451": "UNAVAILABLE FOR LEGAL REASONS",
    "422": "UNPROCESSABLE ENTITY",
    "415": "UNSUPPORTED MEDIA TYPE",
    "426": "UPGRADE REQUIRED",
    "305": "USE PROXY",
    "506": "VARIANT ALSO NEGOTIATES"
}

mimetype_list = {
    "js": "application/javascript",
    "mjs": "application/javascript",
    "json": "application/json",
    "webmanifest": "application/manifest+json",
    "doc": "application/msword",
    "dot": "application/msword",
    "wiz": "application/msword",
    "bin": "application/octet-stream",
    "a": "application/octet-stream",
    "dll": "application/octet-stream",
    "exe": "application/octet-stream",
    "o": "application/octet-stream",
    "obj": "application/octet-stream",
    "so": "application/octet-stream",
    "oda": "application/oda",
    "pdf": "application/pdf",
    "p7c": "application/pkcs7-mime",
    "ps": "application/postscript",
    "ai": "application/postscript",
    "eps": "application/postscript",
    "m3u": "application/vndapplempegurl",
    "m3u8": "application/vndapplempegurl",
    "xls": "application/vndms-excel",
    "xlb": "application/vndms-excel",
    "ppt": "application/vndms-powerpoint",
    "pot": "application/vndms-powerpoint",
    "ppa": "application/vndms-powerpoint",
    "pps": "application/vndms-powerpoint",
    "pwz": "application/vndms-powerpoint",
    "wasm": "application/wasm",
    "bcpio": "application/x-bcpio",
    "cpio": "application/x-cpio",
    "csh": "application/x-csh",
    "dvi": "application/x-dvi",
    "gtar": "application/x-gtar",
    "hdf": "application/x-hdf",
    "latex": "application/x-latex",
    "mif": "application/x-mif",
    "cdf": "application/x-netcdf",
    "nc": "application/x-netcdf",
    "p12": "application/x-pkcs12",
    "pfx": "application/x-pkcs12",
    "ram": "application/x-pn-realaudio",
    "pyc": "application/x-python-code",
    "pyo": "application/x-python-code",
    "sh": "application/x-sh",
    "shar": "application/x-shar",
    "swf": "application/x-shockwave-flash",
    "sv4cpio": "application/x-sv4cpio",
    "sv4crc": "application/x-sv4crc",
    "tar": "application/x-tar",
    "tcl": "application/x-tcl",
    "tex": "application/x-tex",
    "texi": "application/x-texinfo",
    "texinfo": "application/x-texinfo",
    "roff": "application/x-troff",
    "t": "application/x-troff",
    "tr": "application/x-troff",
    "man": "application/x-troff-man",
    "me": "application/x-troff-me",
    "ms": "application/x-troff-ms",
    "ustar": "application/x-ustar",
    "src": "application/x-wais-source",
    "xsl": "application/xml",
    "rdf": "application/xml",
    "wsdl": "application/xml",
    "xpdl": "application/xml",
    "zip": "application/zip",
    "au": "audio/basic",
    "snd": "audio/basic",
    "mp3": "audio/mpeg",
    "mp2": "audio/mpeg",
    "aif": "audio/x-aiff",
    "aifc": "audio/x-aiff",
    "aiff": "audio/x-aiff",
    "ra": "audio/x-pn-realaudio",
    "wav": "audio/x-wav",
    "bmp": "image/x-ms-bmp",
    "gif": "image/gif",
    "ief": "image/ief",
    "jpg": "image/jpeg",
    "jpe": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "svg": "image/svg+xml",
    "tiff": "image/tiff",
    "tif": "image/tiff",
    "ico": "image/vndmicrosofticon",
    "ras": "image/x-cmu-raster",
    "pnm": "image/x-portable-anymap",
    "pbm": "image/x-portable-bitmap",
    "pgm": "image/x-portable-graymap",
    "ppm": "image/x-portable-pixmap",
    "rgb": "image/x-rgb",
    "xbm": "image/x-xbitmap",
    "xpm": "image/x-xpixmap",
    "xwd": "image/x-xwindowdump",
    "eml": "message/rfc822",
    "mht": "message/rfc822",
    "mhtml": "message/rfc822",
    "nws": "message/rfc822",
    "css": "text/css",
    "csv": "text/csv",
    "html": "text/html",
    "htm": "text/html",
    "txt": "text/plain",
    "bat": "text/plain",
    "c": "text/plain",
    "h": "text/plain",
    "ksh": "text/plain",
    "pl": "text/plain",
    "rtx": "text/richtext",
    "tsv": "text/tab-separated-values",
    "py": "text/x-python",
    "etx": "text/x-setext",
    "sgm": "text/x-sgml",
    "sgml": "text/x-sgml",
    "vcf": "text/x-vcard",
    "xml": "text/xml",
    "mp4": "video/mp4",
    "mpeg": "video/mpeg",
    "m1v": "video/mpeg",
    "mpa": "video/mpeg",
    "mpe": "video/mpeg",
    "mpg": "video/mpeg",
    "mov": "video/quicktime",
    "qt": "video/quicktime",
    "webm": "video/webm",
    "avi": "video/x-msvideo",
    "movie": "video/x-sgi-movie"
}

class Response:
    
    def __init__(self, body: str="",
                headers: Union[dict[str, str], None]=None,
                status_code: int=200,
                content_type: str="text/plain"):
        self.status_code    = status_code
        self.status_message = status_list[str(self.status_code)]
        self.content_type   = content_type if "/" in content_type else mimetype_list.get(content_type, "text/plain")
        self.headers        = {}
        self.set_headers({ "Content-Type": f"{self.content_type}; charset=utf-8", "Server": "Python/Tea" })
        if headers:
            self.set_headers(headers)
        self.body = body
        
    
    def __get_headers_as_string(self) -> str:
        return "\r\n".join([f"{key.replace('-', ' ').title().replace(' ', '-')}: {self.headers[key]}" for key in list(self.headers.keys())])
        
    
    def get_res_as_text(self) -> str:
        """
        Get raw response text as string.
        """
        self.set_headers({ "Content-Length": len(self.body), "Date": datetime.now() })
        return f"HTTP/1.1 {self.status_code} {status_list[str(self.status_code)]}\r\n{self.__get_headers_as_string()}\r\n\r\n{self.body}"
    
    
    def set_header(self, key: str, value: str) -> None:
        """
        Add new header to response.
        """
        self.headers[key.replace("-", " ").title().replace(" ", "-")] = value
                
    
    def set_headers(self, headers: dict[str, str]) -> None:
        """
        Add multiple headers as dict to response.
        """
        for key in headers:
            self.headers[key.replace("-", " ").title().replace(" ", "-")] = headers[key]
                
    
    def send(self, body: str="",
            headers: Union[dict[str, str], None]=None,
            status_code: int=200,
            content_type: str="text/plain") -> None:
        """
        Send response inside the callback function.
        """
        self.status_code    = status_code
        self.status_message = status_list[str(self.status_code)]
        self.content_type   = content_type if "/" in content_type else mimetype_list.get(content_type, "text/plain")
        self.set_header("Content-Type", f"{self.content_type}; charset=utf-8")
        if headers:
            self.set_headers(headers)
        self.body = body
        
    
    def send_file(self, filename: str,
                headers: dict[str, str]=None,
                status_code: int=200) -> None:
        """
        Send file as response inside the callback function with auto content type.
        """
        self.status_code    = status_code
        self.status_message = status_list[str(self.status_code)]
        self.content_type   = mimetype_list.get(filename.split(".")[-1], "text/plain")
        self.set_header("Content-Type", f"{self.content_type}; charset=utf-8")
        if headers:
            self.set_headers(headers)
        
        absolute_path = Path(filename).resolve()
        try:
            with open(absolute_path, "r", encoding="utf-8") as f:
                self.body = f.read()
        except Exception as e:
            raise
