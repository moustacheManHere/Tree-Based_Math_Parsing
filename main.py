import sys; sys.dont_write_bytecode = True

import Ligma

if __name__ == "__main__":

    prog = Ligma.Ballz()
    prog.output.print_start()
    prog.run()
    prog.output.print_end()