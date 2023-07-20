printc() {
  if [ "$2" = "info" ]; then
    COLOR="96m" # light blue
  elif [ "$2" = "success" ]; then
    COLOR="92m" # green
  elif [ "$2" = "warning" ]; then
    COLOR="93m" # yellow
  elif [ "$2" = "danger" ]; then
    COLOR="91m" # red
  else
    COLOR="0m" # no (default) color
  fi

  START_COLOR="\e[$COLOR"
  END_COLOR="\e[0m"
  printf "$START_COLOR%b$END_COLOR" "$1"
}

bool() {
  [ $(echo "$1" | tr "[:lower:]" "[:upper:]") = "TRUE" ] && echo true || echo false
}
