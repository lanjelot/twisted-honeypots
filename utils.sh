#!/bin/bash

usage()
{
  echo "$0 <stats|extract> [max_count]"
  exit 2
}

(( $# < 3 )) || usage

action=$1
max=$2
limit="limit 0,${max:-10}"

EXPORT_PATH=$HOME/pots

case $action in
  extract) 
    names='combo password login'
    [[ -z $max ]] && limit=""
    [[ -d $EXPORT_PATH ]] || mkdir $EXPORT_PATH
  ;;
  *) 
    action='stats'
    names='combo password login host'
  ;;
esac

for what in $names; do
  if [[ $what == 'combo' ]]; then
    name='concat_ws(char(58),login,password)' 
  else
    name=$what
  fi

  if [[ $action = 'stats' ]]; then
    echo "* Top $max ${what}s"
    echo "select count(2), $name from pot group by 2 order by count(2) desc $limit" | mysql -rs -upot_user -ppassword pot_db 
    echo
  else
    echo "select $name from pot" | mysql -rs -upot_user -ppassword pot_db > $EXPORT_PATH/pot_$what.all
    echo "select $name from pot group by 1 order by count(1) desc $limit" | mysql -rs -upot_user -ppassword pot_db > $EXPORT_PATH/pot_$what.dic
  fi
done

if [[ $action = 'stats' ]]; then
  echo '* Last SSH attacks'
  tail /var/log/ssh-pot.log
  echo

  echo '* Last FTP attacks'
  tail /var/log/ftp-pot.log
  echo

  echo '* Last Telnet attacks'
  tail /var/log/telnet-pot.log
  echo

  echo '* Total records'
  echo 'select count(*) from pot' | mysql -rs -upot_user -ppassword pot_db

fi
