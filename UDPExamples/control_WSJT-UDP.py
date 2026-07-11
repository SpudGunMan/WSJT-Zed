#!/usr/bin/env python3
# WSJT-Z Control via UDP
# Schema 3+ support for remote AutoCQ/AutoCall mode control
# DE K7MHI

import socket
import struct
import sys
import argparse
from enum import IntEnum

class MessageType(IntEnum):
    """WSJT-Z UDP Message Types"""
    Heartbeat = 0
    Status = 1
    Decode = 2
    Clear = 3
    Reply = 4
    QSOLogged = 5
    Close = 6
    Replay = 7
    HaltTx = 8
    FreeText = 9
    WSPRDecode = 10
    Location = 11
    LoggedADIF = 12
    HighlightCallsign = 13
    SwitchConfiguration = 14
    Configure = 15
    AnnotationInfo = 16
    # Future message types would go here


class QtDataStreamWriter:
    """Writes Qt-compatible binary data streams (big-endian)"""
    
    def __init__(self):
        self.data = bytearray()
    
    def write_uint32(self, value):
        self.data.extend(struct.pack('>I', value))
    
    def write_int32(self, value):
        self.data.extend(struct.pack('>i', value))
    
    def write_uint8(self, value):
        self.data.extend(struct.pack('>B', value))
    
    def write_bool(self, value):
        self.data.extend(struct.pack('>B', 1 if value else 0))
    
    def write_double(self, value):
        self.data.extend(struct.pack('>d', value))
    
    def write_utf8(self, text):
        """Write a UTF-8 string as QByteArray (size-prefixed)"""
        if text is None:
            self.write_uint32(0xffffffff)  # null string
        else:
            encoded = text.encode('utf-8')
            self.write_uint32(len(encoded))
            self.data.extend(encoded)
    
    def get_bytes(self):
        return bytes(self.data)


def build_configure_message(message_id, mode='', frequency_tolerance=0xffffffff, 
                           submode='', fast_mode=False, tr_period=0xffffffff,
                           rx_df=0xffffffff, dx_call='', dx_grid='', 
                           generate_messages=False, auto_cq_enabled=False, auto_call_enabled=False,
                           schema=None):
    """
    Build a Configure message to send to WSJT-Z
    
    Args:
        message_id: Identifier for this control client
        mode: Mode to set (empty = no change)
        frequency_tolerance: Frequency tolerance in Hz (0xffffffff = no change)
        submode: Submode character (empty = no change)
        fast_mode: Enable fast mode
        tr_period: T/R period in seconds (0xffffffff = no change)
        rx_df: RX audio frequency offset (0xffffffff = no change)
        dx_call: DX call to work (empty = no change)
        dx_grid: DX grid locator (empty = no change)
        generate_messages: Generate standard messages automatically
        auto_cq_enabled: Enable AutoCQ mode
        auto_call_enabled: Enable AutoCall mode
        schema: Schema version (None = auto-detect, 2 = legacy, 3 = with AutoCQ/AutoCall)
    """
    
    writer = QtDataStreamWriter()
    
    # Auto-detect schema: use 3 only if AutoCQ/AutoCall fields are being set
    if schema is None:
        schema = 3 if (auto_cq_enabled or auto_call_enabled) else 2
    
    # Header
    writer.write_uint32(0xadbccbda)  # magic number
    writer.write_uint32(schema)  # schema version
    
    # Message type and ID
    writer.write_uint32(MessageType.Configure)
    writer.write_utf8(message_id)
    
    # Payload: Configure message fields (schema 2)
    writer.write_utf8(mode)
    writer.write_uint32(frequency_tolerance)
    writer.write_utf8(submode)
    writer.write_bool(fast_mode)
    writer.write_uint32(tr_period)
    writer.write_uint32(rx_df)
    writer.write_utf8(dx_call)
    writer.write_utf8(dx_grid)
    writer.write_bool(generate_messages)
    
    # Schema 3+ fields: AutoCQ/AutoCall control (only if schema >= 3)
    if schema >= 3:
        writer.write_bool(auto_cq_enabled)
        writer.write_bool(auto_call_enabled)
    
    return writer.get_bytes()


def send_configure_message(server_address, server_port, message_id, **kwargs):
    """Send a Configure message to WSJT-X"""
    
    message = build_configure_message(message_id, **kwargs)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message, (server_address, server_port))
        sock.close()
        return True
    except Exception as e:
        print(f"Error sending message: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    # Default configuration
    DEFAULT_SERVER = 'localhost'
    DEFAULT_PORT = 2237
    DEFAULT_ID = 'ControlClient'
    
    parser = argparse.ArgumentParser(
        description='Control WSJT-X AutoCQ/AutoCall modes via UDP',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Enable AutoCQ only
  %(prog)s --auto-cq
  
  # Enable AutoCall only
  %(prog)s --auto-call
  
  # Disable both
  %(prog)s --no-auto-cq --no-auto-call
  
  # Control remote WSJT-X instance
  %(prog)s --host 192.168.1.100 --auto-cq
  
  # Send with mode change
  %(prog)s --mode FT4 --auto-cq
        ''')
    
    parser.add_argument('--host', default=DEFAULT_SERVER,
                       help=f'WSJT-X server address (default: {DEFAULT_SERVER})')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT,
                       help=f'WSJT-X UDP port (default: {DEFAULT_PORT})')
    parser.add_argument('--id', default=DEFAULT_ID,
                       help=f'Client identifier (default: {DEFAULT_ID})')
    
    parser.add_argument('--auto-cq', action='store_true',
                       help='Enable AutoCQ mode')
    parser.add_argument('--no-auto-cq', action='store_true',
                       help='Disable AutoCQ mode')
    parser.add_argument('--auto-call', action='store_true',
                       help='Enable AutoCall mode')
    parser.add_argument('--no-auto-call', action='store_true',
                       help='Disable AutoCall mode')
    
    parser.add_argument('--mode', default='',
                       help='Mode to set (e.g., FT4, FT8, JT65)')
    parser.add_argument('--freq-tol', type=int, default=0xffffffff,
                       help='Frequency tolerance in Hz (default: no change)')
    parser.add_argument('--rx-df', type=int, default=0xffffffff,
                       help='RX audio frequency offset (default: no change)')
    parser.add_argument('--tr-period', type=int, default=0xffffffff,
                       help='T/R period in seconds (default: no change)')
    parser.add_argument('--dx-call', default='',
                       help='DX call to work (default: no change)')
    parser.add_argument('--dx-grid', default='',
                       help='DX grid locator (default: no change)')
    parser.add_argument('--generate-messages', action='store_true',
                       help='Enable automatic message generation')
    parser.add_argument('--schema', type=int, choices=[2, 3], default=None,
                       help='Schema version (default: auto-detect based on fields)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show message details')
    
    args = parser.parse_args()
    
    # Handle AutoCQ/AutoCall flags
    auto_cq = None
    auto_call = None
    
    if args.auto_cq:
        auto_cq = True
    elif args.no_auto_cq:
        auto_cq = False
    
    if args.auto_call:
        auto_call = True
    elif args.no_auto_call:
        auto_call = False
    
    # Build message
    kwargs = {
        'mode': args.mode,
        'frequency_tolerance': args.freq_tol,
        'rx_df': args.rx_df,
        'tr_period': args.tr_period,
        'dx_call': args.dx_call,
        'dx_grid': args.dx_grid,
        'generate_messages': args.generate_messages,
        'schema': args.schema,
    }
    
    if auto_cq is not None:
        kwargs['auto_cq_enabled'] = auto_cq
    if auto_call is not None:
        kwargs['auto_call_enabled'] = auto_call
    
    # Show what we're doing
    if args.verbose:
        print("=" * 60)
        print("WSJT-X UDP Configure Message")
        print("=" * 60)
        print(f"Target: {args.host}:{args.port}")
        print(f"Client ID: {args.id}")
        # Determine actual schema that will be used
        actual_schema = args.schema if args.schema else (3 if (auto_cq is True or auto_call is True) else 2)
        print(f"Schema: {actual_schema}")
        print()
        if auto_cq is not None:
            print(f"AutoCQ:   {'ENABLE' if auto_cq else 'DISABLE'}")
        if auto_call is not None:
            print(f"AutoCall: {'ENABLE' if auto_call else 'DISABLE'}")
        if args.mode:
            print(f"Mode:     {args.mode}")
        if args.dx_call:
            print(f"DX Call:  {args.dx_call}")
        print()
    
    # Send message
    if send_configure_message(args.host, args.port, args.id, **kwargs):
        if args.verbose:
            print("✓ Configure message sent successfully")
        else:
            print("OK")
        sys.exit(0)
    else:
        print("✗ Failed to send configure message", file=sys.stderr)
        sys.exit(1)
