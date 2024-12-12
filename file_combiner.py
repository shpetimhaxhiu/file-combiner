# file_combiner.py

import os
import glob
import json
import logging
import sys
from typing import Dict, List, Any
from pathlib import Path
import argparse
from json.decoder import JSONDecodeError

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('file_combiner.log')
    ]
)
logger = logging.getLogger(__name__)

def validate_config(config: Dict[str, Any]) -> bool:
    """Validate the configuration structure."""
    try:
        required_keys = {'fileGroups'}
        if not all(key in config for key in required_keys):
            raise ValueError(f"Missing required keys: {required_keys - set(config.keys())}")

        for group in config['fileGroups']:
            # 'fileGlobs' is not always required; either 'fileGlobs' or 'files' is acceptable.
            group_required_keys = {'fileHeader', 'entryHeader', 'entryFooter', 'fileFooter'}
            if not all(key in group for key in group_required_keys):
                raise ValueError(f"File group missing required keys: {group_required_keys - set(group.keys())}")

            # At least one of fileGlobs or files must be present
            if not ('fileGlobs' in group or 'files' in group):
                raise ValueError("File group must have either 'fileGlobs' or 'files' defined")

        return True
    except Exception as e:
        logger.error(f"Configuration validation failed: {str(e)}")
        return False

def read_config(config_path: str) -> Dict[str, Any]:
    """Read and parse the configuration file."""
    try:
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with config_path.open('r', encoding='utf-8') as file:
            config = json.load(file)
            
        if not validate_config(config):
            raise ValueError("Invalid configuration structure")
            
        return config
    except JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error reading config: {str(e)}")
        raise

def write_section(file, lines: List[str], context: str = '') -> None:
    """Write a section of lines to the file with error handling."""
    try:
        for line in lines:
            file.write(line + '\n')
    except Exception as e:
        logger.error(f"Error writing {context}: {str(e)}")
        raise

def write_toc(file, toc: Dict[str, Any], toc_entries: List[Dict[str, Any]]) -> None:
    """Write table of contents with error handling."""
    try:
        write_section(file, toc['tocHeader'], 'TOC header')
        for entry in toc_entries:
            line = toc['tocEntry'].replace('${lineNo}', str(entry['lineNo'])).replace('${entryPath}', entry['entryPath'])
            file.write(line + '\n')
        write_section(file, toc['tocFooter'], 'TOC footer')
    except Exception as e:
        logger.error(f"Error writing TOC: {str(e)}")
        raise

def combine_files(config: Dict[str, Any], output_path: str = 'combined_output.txt') -> None:
    """Combine files according to configuration."""
    output_path = Path(output_path)
    
    try:
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with output_path.open('w', encoding='utf-8') as outfile:
            for group in config['fileGroups']:
                write_section(outfile, group['fileHeader'], 'file header')
                toc_entries = []
                line_no = len(group['fileHeader']) + 1

                # Gather files from either fileGlobs or files
                file_list = []
                if 'fileGlobs' in group:
                    for pattern in group['fileGlobs']:
                        for filepath in glob.glob(pattern, recursive=True):
                            file_list.append(filepath)
                elif 'files' in group:
                    file_list = group['files']

                for filepath_str in file_list:
                    filepath = Path(filepath_str)
                    if not filepath.exists():
                        logger.warning(f"Skipping non-existent file: {filepath}")
                        continue

                    logger.info(f"Processing file: {filepath}")
                    toc_entries.append({'lineNo': line_no, 'entryPath': str(filepath)})

                    # Write entry header
                    entry_header = [line.replace('${entryPath}', str(filepath)) for line in group['entryHeader']]
                    write_section(outfile, entry_header, 'entry header')
                    line_no += len(entry_header)

                    # Write file content
                    with filepath.open('r', encoding='utf-8') as infile:
                        for line in infile:
                            outfile.write(line)
                            line_no += 1

                    # Write entry footer
                    entry_footer = [line.replace('${entryPath}', str(filepath)) for line in group['entryFooter']]
                    write_section(outfile, entry_footer, 'entry footer')
                    line_no += len(entry_footer)

                if group.get('includeToc', False):
                    write_toc(outfile, group, toc_entries)
                    line_no += len(group['tocHeader']) + len(group['tocFooter']) + len(toc_entries)

                write_section(outfile, group['fileFooter'], 'file footer')

        logger.info(f"Successfully created combined file at: {output_path}")

    except Exception as e:
        logger.error(f"Error combining files: {str(e)}")
        raise

def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description='Combine files based on configuration')
    parser.add_argument('--config', '-c', default='configfile.json', help='Path to configuration file')
    parser.add_argument('--output', '-o', default='combined_output.txt', help='Output file path')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logger.setLevel(logging.DEBUG)

    try:
        config = read_config(args.config)
        combine_files(config, args.output)
    except Exception as e:
        logger.error(f"Program failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
