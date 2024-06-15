This file describes project structure and methodology.

### How to Build:

On a fresh repository, we need to download python packages our project uses. This is installed in venv/ and only needs to be created once unless you added a new import. Command to create venv:\
`make venv`

src/main.py is the entry point. The run command is:\
`python3 src/main.py`

(make sure you are at the root of the project when calling this)

### Project Structure:

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


In the future, it should be called using presets (initial car positions, speeds). These presets will be defined under presets/.

`python3 src/main.py presets/example_preset`

#### `src/classes`
- contains classes that may be used by all other files. Vehicle is an example of a class.

#### `src/simulator`
- contains files responsible for running pygame and the world simulation. It should contain methods for how to render vehicles, and this should not fall under the responsibility of vehicle.py or any other files in classes/.
- `src/simulator/simulator.py` is especially important as this is where the game loop occurs. All updating and rendering functions are called here.

#### `src/manager`
- contains files responsible for the manager. This is the brain of concurrent-traffic performing calculations, such as determining if cars are on a path to collide, deciding what adjustments cars need to make to speed, etc.

### Conventions:
We want to keep our project clean and consistent, so please adhere to these conventions.
- Naming:
  - for variables, words should be separated by underscore. Not camelCase.
  - constants are all capital
- Functional approach. We are not taking object-oriented approach. This means no class should have their own functions where it uses member variables. Instead, functions should be defined in the same file, and take in the object as a parameter.