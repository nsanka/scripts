#!/bin/tclsh
# Version 1.3
# Author:: Naga Sanka (nsanka@me.com)
# Sep 19, 2013

# Updates:
# Jun 07, 2013 - Created this script to delete the files of particular extension
#	Jun 07, 2013 - Delete All, One by One (C option)
#	Jun 20, 2013 - Added all files to be deleted in a text file and open the file in text editor
#	Jun 26, 2013 - Added delete empty folders
#	Sep 19, 2013 - Added to delete the folders that has a common keyword

###################################### CHECK/UPDATE #######################################
set checkPath "/home/user"
set match "rpm"; # Extension with dot or Part of the name of Folder
set userName "userName"; # UserName
set tecmd "vim"; # Text Editor command
set delTempFile "Y"; # Delete the text file (list of files to be deleted) created by this script
##################################### END OF CHECK/UPDATE #################################

################################ DO NOT CHANGE ANYTHING BELOW #############################
# Delete Empty Folders
catch {exec find $checkPath -type d -empty -user $userName} foldersPathList
if {[llength $foldersPathList] > 0} {
   puts "Following folders will be deleted"
   puts "####################################################################"
   foreach folderPath $foldersPathList {
      puts "$folderPath"
      }
   puts "####################################################################"
   puts -nonewline "There are [llength $foldersPathList] of empty folders in $checkPath, Delete All? (Y/N) - "
   flush stdout
   set Ans [gets stdin]
   if {$Ans == "Y"} {
      foreach folderPath $foldersPathList {
         puts "Deleting $folderPath"
         file delete -force $folderPath
         }
      }
   } else {
      puts "There are no empty folders in $checkPath"
      }

# Delete Files
catch {exec find $checkPath -type f -user $userName} filesPathList
set df "delete_files.txt"
set wf [open $df "w"]
set cnt 0
set reqFilePathList ""
foreach filePath $filesPathList {
   set filename [lindex [split $filePath "/"] end]
   if {$match == ".[lindex [split $filename "."] end]"} {
      lappend reqFilePathList $filePath
      puts $wf $filePath
      incr cnt
      }
   }
# Delete Folders
catch {exec find $checkPath -type d -user $userName} foldersPathList
foreach folderPath $foldersPathList {
   set foldername [lindex [split $folderPath "/"] end]
   if {[string match "*$match*" $foldername]} {
      lappend reqFilePathList $folderPath
      puts $wf $folderPath
      incr cnt
      }
   }
close $wf
if {$cnt > 0} {
   puts "####################################################################"
   puts -nonewline "Do you want to see the files/folders to be deleted? (Y/N) - "
   flush stdout
   set Ans [gets stdin]
   if {$Ans == "Y"} {
      exec $tecmd $df &
      }
   puts "####################################################################"
   puts -nonewline "There are $cnt of $match files/folders in $checkPath, Delete All? (Y/N/C) - "
   flush stdout
   set Answer [gets stdin]
   if {$Answer != "N"} {
      foreach filePath $reqFilePathList {
         if {$Answer == "C"} {
            puts -nonewline "Delete $filePath? (Y/N) - "
            flush stdout
            set Answer1 [gets stdin]
            if {$Answer1 == "Y"} {
               puts "Deleting $filePath"
               file delete $filePath
               }
            }
         if {$Answer == "Y"} {
            puts "Deleting $filePath"
            file delete $filePath
            }
         }
      }
   } else {
      puts "There are no $match files in $checkPath"
      }
if {$delTempFile == "Y"} {
   puts "Deleting $df the temporary file created"
   file delete $df
   }
########################################### END OF SCRIPT ######################################
