ENCODE2BDBag Service
--------------------

This service uses the encode2bag tool to create a BDBag for a given ENCODE query or metadata file. 
The resulting BDBag includes references to the files represented by that query, at that point in time. 
The BDBag is uploaded to S3 where it can be downloaded directly, or via Globus. The BDBag is also
associated a Minid identifer via which it can be unambiguously named and referenced. 

The running service is avaialble at: http://encode.bdbag.org/

