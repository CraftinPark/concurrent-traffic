This file describes project structure.

```
concurrent-traffic/
│
└── src/
    ├── classes/
        └── ...
    ├── manager/
        └── ...
    ├── simulator/
        └── ...
    └── main.py
```

src/main.py is the entry point. The run command is:

```python3 src/main.py```

In the future, it should be called using presets (initial car positions, speeds). These presets will be defined under presets/.

```python3 src/main.py presets/example_preset```

```src/classes``` contains classes that may be used by all other files. Vehicle is an example of a class

```src/simulator``` contains files responsible for running pygame and the world simulation. It should contain methods for how to render vehicles, and this should not fall under the responsibility of vehicle.py or any other files in classes/.

```src/manager``` contains files responsible for the manager. This is the brain of concurrent-traffic performing all kinds of calculations, such as determining if cars are on a path to collide, deciding what adjustments cars need to make to speed, etc.

