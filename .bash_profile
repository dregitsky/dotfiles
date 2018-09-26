source ~/git-completion.bash
encrypt() { openssl aes-256-cbc -a -salt -in "$1" -out "$1.encrypted"; }
decrypt() { 
  name="$1"
  suffix=".encrypted"
  basefile=${name%"$suffix"}
  openssl aes-256-cbc -d -a -salt -in "$1" -out "$basefile"
}
