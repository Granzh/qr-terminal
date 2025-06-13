#!/usr/bin/env python3
"""
QR Terminal - Generate QR codes in terminal from piped input
"""

import sys
import argparse
import os
from typing import Optional, Union
import qrcode
from qrcode.console_scripts import main as qr_main
from qrcode.image.pure import PyPNGImage


__version__ = "1.0.0"


class QRGenerator:
    ERROR_LEVELS = {
        'L': qrcode.constants.ERROR_CORRECT_L,  # ~7%
        'M': qrcode.constants.ERROR_CORRECT_M,  # ~15%
        'Q': qrcode.constants.ERROR_CORRECT_Q,  # ~25%
        'H': qrcode.constants.ERROR_CORRECT_H   # ~30%
    }
    
    def __init__(self, error_correction='M', border=4, box_size=1, version=1):
        self.qr = qrcode.QRCode(
            version=version,
            error_correction=self.ERROR_LEVELS.get(error_correction, qrcode.constants.ERROR_CORRECT_M),
            box_size=box_size,
            border=border,
        )
    
    def generate_terminal(self, data: str, invert: bool = True, colored: bool = False) -> None:
        self.qr.clear()
        self.qr.add_data(data)
        self.qr.make(fit=True)
        
        if colored:
            self._print_colored_ascii(invert)
        else:
            self.qr.print_ascii(invert=invert)
    
    def save_to_file(self, data: str, filename: str, format: str = 'PNG') -> None:
        self.qr.clear()
        self.qr.add_data(data)
        self.qr.make(fit=True)
        
        if format.upper() == 'PNG':
            img = self.qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
        elif format.upper() == 'SVG':
            from qrcode.image.svg import SvgPathImage
            img = self.qr.make_image(image_factory=SvgPathImage)
            img.save(filename)
        else:
            raise ValueError(f"Unknow format: {format}")


def get_input_data(text: Optional[str]) -> str:
    if text:
        return text
    
    if sys.stdin.isatty():
        raise ValueError("Empty data for encode (use pipeline or arg)")
    
    try:
        data = sys.stdin.read().strip()
        if not data:
            raise ValueError("Empty data from stdin")
        return data
    except KeyboardInterrupt:
        print("\nAborted", file=sys.stderr)
        sys.exit(1)


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='qr',
        description='Generation of QR from stdin or args',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
usage examples:
  echo "Hello World" | qr
  qr "Hello World"
  curl -s https://example.com | qr -c
  cat file.txt | qr -e H -b 2
  ip addr show | qr --output qr.png
  echo "WIFI:T:WPA;S:MyNetwork;P:password;;" | qr
  
Version: {__version__}
        """
    )
    
    parser.add_argument(
        'text', 
        nargs='?', 
        help='text for encode (if empty reading from pipeline)'
    )
    
    qr_group = parser.add_argument_group('QR-code parameters')
    qr_group.add_argument(
        '-e', '--error-correction',
        choices=['L', 'M', 'Q', 'H'],
        default='M',
        help='Errors correction levels: L(~7%%), M(~15%%), Q(~25%%), H(~30%%) (default: M)'
    )
    
    qr_group.add_argument(
        '-b', '--border',
        type=int,
        default=4,
        help='size of the border (default: 4)'
    )
    
    qr_group.add_argument(
        '-s', '--box-size',
        type=int,
        default=1,
        help='block size (default: 1)'
    )
    
    qr_group.add_argument(
        '-v', '--version',
        type=int,
        default=1,
        choices=range(1, 41),
        help='version of qr-code (1-40, default: 1 - auto-definition)'
    )
    
    # Параметры отображения
    display_group = parser.add_argument_group('display options')
    display_group.add_argument(
        '-i', '--invert',
        action='store_true',
        help='invert colors (white background)'
    )
    
    output_group = parser.add_argument_group('output parameters')
    output_group.add_argument(
        '-o', '--output',
        help='save to file (.png, .svg)'
    )
    
    output_group.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='only qr-code output'
    )
    
    parser.add_argument(
        '--version-info',
        action='version',
        version=f'qr-terminal {__version__}'
    )
    
    return parser


def main():
    """main CLI function"""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        data = get_input_data(args.text)
        
        if not args.quiet and not args.output:
            data_info = f"data: {len(data)} symbols"
            if len(data) > 50:
                preview = data[:47] + "..."
            else:
                preview = data
            
            print(f"{data_info}", file=sys.stderr)
            print(f"input: {preview}", file=sys.stderr)
            print(f"QR-code:", file=sys.stderr)
            print("", file=sys.stderr)
        
        generator = QRGenerator(
            error_correction=args.error_correction,
            border=args.border,
            box_size=args.box_size,
            version=args.version
        )
        
        if args.output:
            ext = os.path.splitext(args.output)[1].lower()
            if ext == '.png':
                format_type = 'PNG'
            elif ext == '.svg':
                format_type = 'SVG'
            else:
                format_type = 'PNG'
                if not args.quiet:
                    print(f"unknow extension, saving as PNG", file=sys.stderr)
            
            generator.save_to_file(data, args.output, format_type)
            if not args.quiet:
                print(f"QR-code saved in: {args.output}", file=sys.stderr)
        else:
            generator.generate_terminal(data, invert=not args.invert)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        if "Empty data for encode" in str(e):
            parser.print_help()
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\naborted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"unknow error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()