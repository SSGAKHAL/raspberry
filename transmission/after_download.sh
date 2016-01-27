#!/bin/bash
TR_CMD="transmission-remote --auth=neptune_torrent:ciaotorrent"
#MOVEDIR=/media/transmission # the folder to move completed downloads to
TORRENTLIST=`$TR_CMD --list | sed --e '1d;$d;s/^ *//' | cut --only-delimited --delimiter=' ' --fields=1`
#INIZIALIZZAZIONE DELLE VARIABILI
INCOMPLETE_VALUE=""
COMPLETE_VALUE=""
INCOMPLETE_COUNT=1
COMPLETE_COUNT=1
FULL_COMPLETE="  Percent Done: 100%"
for TORRENTID in $TORRENTLIST
do

   DL_COMPLETED=`$TR_CMD --torrent $TORRENTID --info | grep "Percent Done: "`
   STATE_STOPPED=`$TR_CMD --torrent $TORRENTID --info | grep "State: "`
   UPLOADED=`$TR_CMD --torrent $TORRENTID --info | grep "Uploaded: "`
   DOWNLOADED=`$TR_CMD --torrent $TORRENTID --info | grep "Downloaded: "`
   TOTAL_SIZE=`$TR_CMD --torrent $TORRENTID --info | grep "Total size: "`
   DATE_ADDED=`$TR_CMD --torrent $TORRENTID --info | grep "Date added: "`
   DATE_FINISHED=`$TR_CMD --torrent $TORRENTID --info | grep "Date finished: "`
   DOWNLOADING_TIME=`$TR_CMD --torrent $TORRENTID --info | grep "Downloading Time: "`
   AVAILABILITY=`$TR_CMD --torrent $TORRENTID --info | grep "Availability: "`
   Name=`$TR_CMD --torrent $TORRENTID --info | grep "Name: "`

 if [  "$Name" != "" ]
   then
         if [ "$DL_COMPLETED" == "$FULL_COMPLETE" ]
          then
   	        var1="\t $COMPLETE_COUNT) $Name, $AVAILABILITY, $DL_COMPLETED, $DOWNLOADED, $UPLOADED, $TOTAL_SIZE, $DATE_ADDED, $DATE_FINISHED, $DOWNLOADING_TIME, $STATE_STOPPED"
		COMPLETE_VALUE="$COMPLETE_VALUE  $var1 \n \n"
		COMPLETE_COUNT=$((COMPLETE_COUNT + 1))
	  else
		var2="\t $INCOMPLETE_COUNT) $Name, $AVAILABILITY, $DL_COMPLETED, $DOWNLOADED, $UPLOADED, $TOTAL_SIZE, $DATE_ADDED, $DATE_FINISHED, $DOWNLOADING_TIME, $STATE_STOPPED"
		INCOMPLETE_VALUE="$INCOMPLETE_VALUE  $var2 \n\n"
		INCOMPLETE_COUNT=$((INCOMPLETE_COUNT + 1))
	  fi
  fi


#   if [[ ( ! -z "$DL_COMPLETED" ) && ( ! -z "$STATE_STOPPED" ) ]]
#   then
#      echo "Torrent #$TORRENTID is completed."
#      echo "Moving downloaded file(s) to $MOVEDIR."
#      $TR_CMD --torrent $TORRENTID --move $MOVEDIR
#      echo "Removing torrent from list."
#      $TR_CMD --torrent $TORRENTID --remove
#   else
#      echo "Torrent #$TORRENTID is not completed. Ignoring."
#   fi
done
DF_H=$(df -h)
DIMENSION_PI="\n La dimensione della raspberry: \n \n $DF_H"
echo -e "La lista dei file nel transimission: \n\n\n \t COMPLETE DOWNLOAD: \n \n $COMPLETE_VALUE \n \n \t INCOMPLETE DOWNLOAD: \n \n $INCOMPLETE_VALUE \n \n $DIMENSION_PI" >> /tmp/transmission_tmp.txt
python /home/neptune_pi/transmission/email_sent.py /tmp/transmission_tmp.txt
rm /tmp/transmission_tmp.txt

