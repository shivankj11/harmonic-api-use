# harmonic-api-use

## Setup
1. Install package
```
git clone https://github.com/shivankj11/harmonic-api-use
```
2. Add Harmonic API key to environment variables as HARMONIC_API_KEY
```
sudo $ echo 'export HARMONIC_API_KEY=YOUR_KEY_HERE' >> .zshrc
```

## Usage

### Query a company from webpage URL
```
python harmonic_api company https://www.website.ai/
```

### Query a person from LinkedIn URL
```
python harmonic_api person https://www.linkedin.com/in/xyz
```

### Search for companies with keywords
```
python harmonic_api keywords robotics
```
#### For several keywords:
```
python harmonic_api keywords "Artifical intelligence,Robotics"
```

### Options

`-o output_file_name`