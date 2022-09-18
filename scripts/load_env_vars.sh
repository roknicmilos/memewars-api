load_environment_variables() {
  # There should be one argument ($1) to this function, and
  # it should be the path to the environment variables file

  printc "Loading environment variables...\n"

  # Show environment variables:
  grep -v '^#' "$1"

  # Export environment variables:
  export $(xargs <"$1")
  printc "\n"
}
