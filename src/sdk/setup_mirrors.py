import logging
import subprocess
from pathlib import Path
from configparser import ConfigParser

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler("env_setup.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def ensure_dir(path: Path):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Created directory: {path}")

def verify_setup(name: str, cmd: list, keyword: str):
    """
    Dynamic verification by running CLI commands and checking output.
    """
    try:
        # Run command to get current config
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
        if keyword in result.stdout:
            logging.info(f"Verification SUCCESS: {name} is using {keyword}")
            return True
        else:
            logging.warning(f"Verification FAILED: {name} keyword '{keyword}' not found in output.")
            return False
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error(f"Verification ERROR: Could not run {name} command. {e}")
        return False

def setup_maven():
    """Configures Maven Aliyun mirror in ~/.m2/settings.xml"""
    m2_dir = Path.home() / ".m2"
    settings_path = m2_dir / "settings.xml"
    content = """<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.2.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.2.0 https://maven.apache.org/xsd/settings-1.2.0.xsd">
    <mirrors>
        <mirror>
            <id>aliyunmaven</id>
            <mirrorOf>central</mirrorOf>
            <name>Aliyun Public Repository</name>
            <url>https://maven.aliyun.com/repository/public</url>
        </mirror>
    </mirrors>
</settings>"""
    try:
        ensure_dir(m2_dir)
        settings_path.write_text(content, encoding='utf-8')
        logging.info("Maven: Aliyun mirror configured.")
        # Verification: Check effective settings for the mirror URL
        verify_setup("Maven", ["mvn", "help:effective-settings"], "maven.aliyun.com")
    except Exception as e:
        logging.error(f"Maven setup failed: {e}")

def setup_gradle():
    """Configures Gradle global init script for Aliyun mirrors"""
    gradle_dir = Path.home() / ".gradle"
    init_gradle = gradle_dir / "init.gradle"
    content = """
allprojects {
    repositories {
        maven { url 'https://maven.aliyun.com/repository/public' }
        maven { url 'https://maven.aliyun.com/repository/google' }
        maven { url 'https://maven.aliyun.com/repository/gradle-plugin' }
        mavenCentral()
        google()
    }
}"""
    try:
        ensure_dir(gradle_dir)
        init_gradle.write_text(content.strip(), encoding='utf-8')
        logging.info("Gradle: Aliyun init script configured.")
        # Verification: Check if init.gradle exists (gradle doesn't have a simple 'config list' for mirrors)
        if init_gradle.exists() and "aliyun" in init_gradle.read_text():
            logging.info("Verification SUCCESS: Gradle init script verified via file content.")
    except Exception as e:
        logging.error(f"Gradle setup failed: {e}")

def setup_pip():
    """Configures Pip to use Aliyun index"""
    # Use standard config path for Windows/Unix for better compatibility
    pip_dir = Path.home() / "pip"
    pip_ini = pip_dir / ("pip.ini" if Path.home().drive else "pip.conf")
    try:
        ensure_dir(pip_dir)
        config = ConfigParser()
        config['global'] = {
            'index-url': 'https://mirrors.aliyun.com/pypi/simple/',
            'trusted-host': 'mirrors.aliyun.com'
        }
        with open(pip_ini, 'w', encoding='utf-8') as f:
            config.write(f)
        logging.info("Pip: Aliyun index configured.")
        # Verification: Use pip config command
        verify_setup("Pip", ["pip", "config", "list"], "mirrors.aliyun.com")
    except Exception as e:
        logging.error(f"Pip setup failed: {e}")

def setup_npm():
    """Configures NPM to use npmmirror.com registry via CLI"""
    try:
        subprocess.run(["npm", "config", "set", "registry", "https://registry.npmmirror.com"], 
                        check=True, capture_output=True)
        logging.info("NPM: Registry set to npmmirror.com")
        # Verification: Get current registry
        verify_setup("NPM", ["npm", "config", "get", "registry"], "npmmirror.com")
    except FileNotFoundError:
        logging.warning("NPM: Command not found. Skipping...")
    except Exception as e:
        logging.error(f"NPM setup failed: {e}")

if __name__ == "__main__":
    logging.info("=== Starting Global Dev Environment Setup ===")
    setup_maven()
    setup_gradle()
    setup_pip()
    setup_npm()
    logging.info("=== Setup Completed. Check env_setup.log for details ===")