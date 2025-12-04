# MLOps Week

## Getting Started

### Clone the Repository

```bash
cd ~/code
git clone git@github.com:vivadata/MLOpengouins.git
cd MLOps_week
```

### Setup Project

```bash
make setup
```

copy .env and modify with your settings:
```
echo "dotenv" >> .envrc
direnv allow
copy .env.copy .env
```


### Next Steps

For detailed guidelines and project instructions, please read [Guidelines.md](./docs/02_Experiment_Tracking_Guidelines.md).
