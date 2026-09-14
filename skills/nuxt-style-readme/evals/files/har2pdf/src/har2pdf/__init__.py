"""Rebuild a paginated e-book from a captured HAR file.

The reader streams one JPEG per page plus a per-title decryption nonce that is
only present in the initial bootstrap response. If the capture starts after that
response, page order cannot be recovered.
"""
