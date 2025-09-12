
import sys
import argparse

def progressbar(
    current:float,
    total:float,
    width:int=50,
    lhs:str=">",
    head:str="|",
    rhs:str="<"
    ) -> None :
    f"""
    Utility to make a progress bar

    Usage:
        {sys.argv[0]} current total [width=<int>] [lhs=<str>] [head=<str>] [rhs=<str>]

    Arguments:
        current Index of the ongoing process
        total   Total number of all processes

    Options:
        width [default=50]    Total number of columns for the bar to take up
        lhs   [default=">"]   Left hand symbol in the progress bar
        head  [default="|"]   Symbol for the current status in the progress bar
        rhs   [default="<"]   Right hand symbol in the progress bar
    """

    percentage = current/total
    currentNumChar = int(percentage*float(width))
    
    outputString = "["
    outputString += lhs * (currentNumChar - 1)
    outputString += head
    outputString += rhs * (int(width) - int(currentNumChar))
    outputString += "]"

    print(f"\r{outputString} {current}/{total} ({int(100*percentage)}%)",end=" ")

    return None

if __name__ == "__main__":
        
    parser = argparse.ArgumentParser(
        description="Utility to make a progress bar",
        epilog=f"Example: python {sys.argv[0]} 69 420 --width 40 --lhs "">"" --head ""|"" --rhs ""<"""
    )
    parser.add_argument(
        "current",
        type=float,
        help="Index of the ongoing process"
    )
    parser.add_argument(
        "total",
        type=float,
        help="Total number of all processes"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=50,
        help=f"[default=50] Total number of columns for the bar to take up"
    )
    parser.add_argument(
        "--lhs",
        type=str,
        default=">",
        help=f"[default=>] Left hand symbol in the progress bar"
    )
    parser.add_argument(
        "--head",
        type=str,
        default="|",
        help=f"[default=|] Symbol for the current status in the progress bar"
    )
    parser.add_argument(
        "--rhs",
        type=str,
        default="<",
        help=f"[default=<] Right hand symbol in the progress bar"
    )

    args = parser.parse_args()
    progressbar(**vars(args))
