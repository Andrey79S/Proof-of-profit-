from core.config_loader import ConfigLoader

loader = ConfigLoader("config")
configs = loader.load_all()

print(configs["equipment"].keys())
print(configs["recipes"].keys())
print(configs["staff"].keys())
