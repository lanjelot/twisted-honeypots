#!/bin/bash


source $(dirname $0)/lib/bashsimplecurses/simple_curses.sh
source $(dirname $0)/vars.sh


EXPORT_PATH=${HOME}/pots

N=60

main(){
	action=$1
	max=$2
	limit="limit 0,${max:-10}"
	action='stats'
	names='combo login password'

	window "Last SSH attacks" "red" "40%"
	tac /var/log/ssh-pot.log | head > /tmp/res
	append_file /tmp/res
	endwin

    window "Last FTP attacks" "red" "40%"
    tac /var/log/ftp-pot.log | head > /tmp/res
	append_file /tmp/res
    endwin

    window "Last Telnet attacks" "red" "40%"
    tac /var/log/telnet-pot.log | head > /tmp/res
	append_file /tmp/res
    endwin

	col_right
	move_up

	for what in $names; do
		if [[ $what == 'combo' ]]; then
			name='concat_ws(char(58),login,password)'
		else
			name=$what
		fi

		window "Top $max ${what}s" "red" "30%"
		echo "select count(2), $name from pot group by 2 order by count(2) desc $limit" | mysql -rs -u${MYSQL_USER} ${MYSQL_DB} > /tmp/res
		append_file /tmp/res
		endwin
	done


  	col_right
	move_up

	window "Top countries" "red" "30%"
	echo "select count(2), host from pot group by 2 order by count(2) desc $limit" | mysql -rs -u${MYSQL_USER} ${MYSQL_DB} | while read i j ; do
		echo "${i}: ${j} ($(geoiplookup $j | sed 's/GeoIP Country Edition: //g'))";
	done > /tmp/res
	append_file /tmp/res
	endwin

	window "Total records" "red" "30%"
	echo "select count(*) from pot" | mysql -rs -upot_user pot_db > /tmp/res
	append_file /tmp/res
	rm /tmp/res
	endwin

	window "Last update" "red" "30%"
	append "$(date) (refresh: ${N}s)"
	endwin
}


main_loop ${N}
