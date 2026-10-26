# Task: Develop a Two-Lecture Python Fundamentals Workshop for Robotics Students

## 1. Background and Teaching Context

I teach a university-level Robotics / Unmanned Systems course primarily attended by senior mechanical engineering students.

A recurring problem is that many students lack fundamental Python programming skills. Rather than understanding how to structure and implement a program, they frequently send entire assignments to AI coding assistants such as Codex.

I want to dedicate two lectures this week to addressing this problem.

**The goal is not to teach an entire introductory programming course.** The goal is to give students enough practical Python literacy that they can read, understand, modify, debug, and write relatively simple programs independently.

The instructional approach should be hands-on, interactive, and grounded in actual robotics applications.

Students already have homework assigned. Do not create additional homework. All exercises must be completed during class.

### Class Schedule

- **Monday:** 75 minutes — Jupyter Notebook
- **Wednesday:** 75 minutes — Python IDE / VS Code

Each lecture must reserve its final **20–25 minutes for an independent programming challenge without AI assistance**.

Students may use instructor-provided notes, reference sheets, and official Python/NumPy documentation, but they cannot use Codex, ChatGPT, or other AI coding assistants during the independent challenges.

## 2. Learning Objectives

By the end of the two lectures, students should be able to:

### Python Fundamentals

1. Declare and manipulate variables.
2. Understand basic Python data types.
3. Use lists, tuples, and NumPy arrays.
4. Write conditional statements using `if`, `elif`, and `else`.
5. Write `for` loops and `while` loops.
6. Understand the difference between fixed iteration and condition-based iteration.
7. Define and call functions.
8. Understand function arguments, parameters, return values, and variable scope.
9. Import libraries and modules.
10. Read and interpret basic Python tracebacks.
11. Understand indexing and common programming errors.

### Object-Oriented Programming

1. Define classes and create objects.
2. Understand constructors using `__init__`.
3. Understand what `self` represents.
4. Distinguish attributes from methods.
5. Understand how objects interact.
6. Understand composition through the "has-a" relationship.
7. Understand inheritance through the "is-a" relationship.
8. Recognize method overriding and basic polymorphism.
9. Import classes from other Python files.

### Robotics Applications

1. Construct a 2D rotation matrix.
2. Transform vectors between body and world coordinate frames.
3. Understand the relationship between orientation and translational motion.
4. Represent planar robot pose using position and heading.
5. Implement basic discrete-time kinematic equations.
6. Simulate planar robot motion.
7. Visualize robot trajectories.
8. Understand how multiple software components form a simple simulator.

Prioritize conceptual understanding over memorizing syntax.

---

# 3. Overall Robotics Application

Build the entire workshop around one continuous example:

**A simplified quadcopter moving in the horizontal XY plane at constant altitude.**

Students should start by rotating a 2D vector on Monday and finish Wednesday with a small working planar robot simulator.

Do not introduce unrelated examples such as bank accounts, animals, employee records, or shopping carts.

Every major Python concept should be demonstrated through robotics.

## Coordinate Conventions

Use a consistent right-handed planar coordinate system:

- World X: Horizontal east/right direction
- World Y: Horizontal north/up direction
- Body X: Robot forward direction
- Body Y: Robot left direction
- Heading/yaw: Counterclockwise-positive from world X
- Angles stored internally in radians
- Positions in meters
- Velocities in meters per second
- Angular velocities in radians per second
- Time in seconds

Use the 2D rotation matrix:

\[
R(\theta)=
\begin{bmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{bmatrix}
\]

Transform body-frame velocity into world-frame velocity:

\[
\mathbf v_w=R(\theta)\mathbf v_b
\]

Use the planar kinematic model:

\[
\dot x=v_x^b\cos\theta-v_y^b\sin\theta
\]

\[
\dot y=v_x^b\sin\theta+v_y^b\cos\theta
\]

\[
\dot\theta=\omega
\]

Use forward Euler integration:

\[
x_{k+1}=x_k+\dot x_k\Delta t
\]

\[
y_{k+1}=y_k+\dot y_k\Delta t
\]

\[
\theta_{k+1}=\theta_k+\omega_k\Delta t
\]

Explain that this is a simplified kinematic model, not a full quadcopter dynamics model.

Assume commanded velocities are achieved instantaneously. Ignore roll, pitch, thrust dynamics, motor dynamics, aerodynamic forces, and altitude changes.

The model should support body-frame lateral motion to represent a holonomic planar approximation.

Introduce a nonholonomic unicycle model later as a comparison, where lateral body-frame velocity is constrained to zero.

---

# 4. Lecture 1 — Monday: Python Fundamentals Through Rotation Matrices

**Duration:** 75 minutes

**Environment:** Jupyter Notebook inside VS Code

**Teaching goal:** Students understand basic Python execution and can write functions and loops that implement 2D coordinate transformations.

## Lecture Schedule

| Time | Topic | Activity |
|---|---|---|
| 0–5 min | Why programming fundamentals matter | Explain coding versus understanding code |
| 5–15 min | Variables, arrays, and imports | Introduce Python and NumPy |
| 15–25 min | Functions and return values | Write a rotation matrix function |
| 25–35 min | Conditionals and for loops | Rotate vectors through multiple angles |
| 35–45 min | While loops and program execution | Introduce repeated state updates |
| 45–50 min | Visualization and debugging | Plot rotated points, inspect errors |
| 50–75 min | Independent challenge | Complete rotation exercise without AI |

The pacing should remain flexible, but protect the final 25 minutes.

## 4.1 Notebook Teaching Style

Create an interactive notebook containing:

- Short Markdown explanations.
- Mathematical equations.
- Small executable code cells.
- Instructor-led examples.
- Predict-the-output questions.
- Short student exercises.
- Deliberate mistakes for debugging.
- Visualizations.
- A final independent challenge.

Avoid large code blocks early in the notebook.

Students should progressively build the final rotation matrix implementation.

Use the following recurring instructional sequence:

**Explain → Predict → Execute → Modify → Verify**

For example, before executing a loop, ask students to predict its output.

## 4.2 Topic A — Imports and Variables

Introduce:

```python
import numpy as np
import matplotlib.pyplot as plt
```

Explain:

- What a library or module is.
- Why libraries are imported.
- What `as np` means.
- How Python locates an imported module.
- The difference between importing and installing a package.
- Why NumPy is useful for vectors and matrices.

Demonstrate basic variables and arrays:

```python
x = 2.0
y = 3.0
theta = 45.0

position = np.array([x, y])
```

Explain how Python lists differ from NumPy arrays, especially for numerical operations.

## 4.3 Topic B — Functions

Teach students how to define and call a function.

Begin with a simple mathematical function, such as converting degrees to radians.

Then introduce a function that constructs a 2D rotation matrix.

Example:

```python
def rotation_matrix(theta):
    c = np.cos(theta)
    s = np.sin(theta)

    return np.array([
        [c, -s],
        [s,  c]
    ])
```

Explicitly explain:

- `def`
- Function name
- Parameters
- Local variables
- `return`
- Calling a function
- The difference between returning and printing values

Explain that `theta` is in radians.

Demonstrate:

```python
theta = np.deg2rad(45)
R = rotation_matrix(theta)
```

Then rotate a point:

```python
point_body = np.array([2.0, 0.0])
point_world = R @ point_body
```

Explain the `@` operator versus `*`.

## 4.4 Topic C — Conditionals

Use robotics-relevant conditions.

Examples:

- Checking whether a robot has reached a target.
- Checking whether a heading angle is valid.
- Checking whether a position is inside a boundary.

Use basic `if`, `elif`, and `else` statements.

Discuss Boolean expressions and indentation.

## 4.5 Topic D — For Loops

Use loops to rotate a body-frame vector through multiple headings.

Example headings:

```python
angles_deg = [0, 45, 90, 135, 180, 270]
```

Students should iterate through the headings, compute rotation matrices, and calculate the transformed vectors.

Teach:

- Iterating over a list.
- `range()`.
- Iterating using indices.
- Loop variables.
- Accumulating results in a list.

Compare a loop against manually repeating the same calculation.

Demonstrate how a `for` loop can generate points along a circular trajectory.

## 4.6 Topic E — While Loops

Introduce a simple simulation clock:

```python
time = 0.0
dt = 0.1

while time < 2.0:
    print(time)
    time += dt
```

Explain:

- Loop conditions.
- Updating variables.
- When a loop terminates.
- Infinite loops.
- Why `while` loops are common in simulations and robotics control.

Keep this section simple.

## 4.7 Topic F — Visualization

Use Matplotlib to show:

1. A body-frame vector.
2. A transformed world-frame vector.
3. Multiple rotated vectors.
4. The circular locus traced by a rotating point.

Use equal aspect ratio so students correctly interpret the geometry.

Provide plotting utilities where appropriate so the focus remains on programming fundamentals.

Explain the difference between computing values and visualizing values.

---

# 5. Monday Independent Challenge — No AI

**Duration:** 20–25 minutes

Students must complete this independently.

## Problem

A quadcopter has a point located 2 meters forward of its center in the body frame.

The quadcopter rotates about its vertical axis while maintaining its world-frame position.

Students must calculate and visualize the point's world-frame location for several orientations.

## Required Tasks

1. Implement a function accepting an angle in degrees.
2. Convert degrees to radians.
3. Construct the correct rotation matrix.
4. Transform the body-frame point into world coordinates.
5. Use a `for` loop to evaluate multiple orientations.
6. Store the transformed points.
7. Plot the points.
8. Verify that the results make physical sense.

Include a basic conditional check, such as validating an input or comparing the rotated point's distance from the origin with its original distance.

## Success Criteria

Students should demonstrate that:

- A 0° rotation leaves the vector unchanged.
- A 90° rotation transforms `[2, 0]` into approximately `[0, 2]`.
- A 180° rotation transforms `[2, 0]` into approximately `[-2, 0]`.
- Rotation preserves vector length.
- The plotted points lie on a circle of radius 2.

Provide starter code with TODO sections.

Do not provide the completed solution in the student notebook.

Provide a separate instructor solution with explanations and tests.

## Difficulty and Scaffolding

Include:

- Required core tasks.
- Optional hints students can reveal or receive from the instructor.
- One stretch task for students who finish early.

Do not make the stretch task necessary for completion.

---

# 6. Lecture 2 — Wednesday: Object-Oriented Programming and Robot Simulation

**Duration:** 75 minutes

**Environment:** VS Code using standard Python `.py` files

**Teaching goal:** Students understand how Python classes interact to build a simple modular robot simulator.

Build directly on Monday's rotation matrix lesson.

Do not restart with a completely unrelated example.

## Lecture Schedule

| Time | Topic | Activity |
|---|---|---|
| 0–5 min | Monday review | Review rotation matrices and functions |
| 5–15 min | Classes and objects | Introduce `Pose2D` |
| 15–25 min | Methods and state | Implement a motion model |
| 25–35 min | Composition | Build the Robot class |
| 35–43 min | Simulator and loops | Introduce the simulation loop |
| 43–50 min | Inheritance and debugging | Compare two motion models |
| 50–75 min | Independent challenge | Modify and run the simulator without AI |

Composition is a primary learning objective.

Inheritance is an instructor-led extension, not the main independent challenge.

---

# 7. Object-Oriented Architecture

Implement multiple small classes rather than placing all behavior inside one giant `Robot` class.

Use the following architecture.

## 7.1 Pose2D

Represents the robot's pose.

Attributes:

- `x`
- `y`
- `yaw`

Students should learn:

- How to define a class.
- What `__init__` does.
- What `self` means.
- How to create an object.
- How to access and modify attributes.

Use an ordinary Python class and explicit constructor for teaching. Avoid introducing dataclasses at this stage.

## 7.2 MotionModel

Base class representing a planar motion model.

Define a consistent method interface such as:

```python
step(pose, vx, vy, omega, dt)
```

The method returns an updated `Pose2D`.

Keep the interface simple. The initial base implementation may raise `NotImplementedError`.

Do not introduce advanced abstract base classes or complex inheritance machinery.

## 7.3 HolonomicModel(MotionModel)

Implements planar motion allowing both forward and lateral body-frame velocities.

Use the rotation matrix to transform body-frame velocity into world-frame velocity.

Use forward Euler integration.

This class should directly reuse concepts from Monday.

## 7.4 UnicycleModel(MotionModel)

Implements a simple nonholonomic motion approximation.

Constrain lateral body-frame velocity to zero:

\[
v_y^b=0
\]

The model should only move along its current heading, while allowing yaw rate commands.

Use the same `step()` interface.

This is an opportunity to explain inheritance, method overriding, and polymorphism.

Make clear that the nonholonomic constraint is an imposed model assumption, not an inherent constraint of a real quadcopter.

## 7.5 Robot

The `Robot` class should use composition.

A Robot **has a**:

- `Pose2D`
- `MotionModel`

The robot should delegate motion calculations to its motion model.

Example conceptual structure:

```python
class Robot:
    def __init__(self, pose, motion_model):
        self.pose = pose
        self.motion_model = motion_model

    def move(self, vx, vy, omega, dt):
        self.pose = self.motion_model.step(
            self.pose, vx, vy, omega, dt
        )
```

Explain why the `Robot` class should not contain every motion equation directly.

Show how the same Robot class can behave differently depending on the motion model assigned to it.

## 7.6 Simulator

The `Simulator` class should own a Robot object and manage the simulation.

Responsibilities:

- Store simulation timestep.
- Advance the robot over time.
- Execute repeated motion updates.
- Maintain trajectory history.
- Provide simulation output for plotting.

Teach the students how the Simulator calls the Robot, and how the Robot delegates motion to the MotionModel.

Keep visualization in a separate helper module.

---

# 8. Composition Versus Inheritance

Explain both concepts explicitly using the simulator.

## Composition — "Has-a"

Examples:

- Simulator has a Robot.
- Robot has a Pose2D.
- Robot has a MotionModel.

## Inheritance — "Is-a"

Examples:

- HolonomicModel is a MotionModel.
- UnicycleModel is a MotionModel.

Introduce basic polymorphism by showing that the Robot can call:

```python
self.motion_model.step(...)
```

without needing to know which specific model is being used.

Students should understand that changing the motion model changes the simulated robot behavior without modifying the Robot class.

Include a clear instructor-facing class relationship diagram.

Distinguish composition arrows from inheritance arrows.

Avoid introducing factories, dependency injection frameworks, advanced interfaces, or elaborate software design patterns.

---

# 9. Wednesday Simulator Demonstration

Create a simple scenario where the robot moves with commanded body-frame velocities.

Example:

```python
vx_body = 1.0
vy_body = 0.5
yaw_rate = 0.2
dt = 0.1
```

Run the same commands through both motion models.

Students should observe:

- The holonomic model can move laterally.
- The unicycle model ignores or constrains lateral velocity.
- Both models can change heading.
- The resulting trajectories differ.

Plot both trajectories using the same axes and equal aspect ratio.

Explain how changing one object affects the behavior of the whole simulation.

## Include a Basic Controller

For the waypoint-following independent exercise, provide a simple prewritten controller or helper function.

The controller may compute world-frame velocity toward a waypoint and convert it into body-frame velocity using the inverse rotation:

\[
\mathbf v_b=R(\theta)^T\mathbf v_w
\]

For the holonomic model, this allows straightforward point-to-point movement while preserving the relevance of rotation matrices.

Keep the controller intentionally simple.

Do not introduce PID, MPC, optimization, or control theory beyond what is necessary.

If yaw is held constant for the waypoint exercise, explain this assumption.

Avoid giving students a task that requires inventing a sophisticated controller during a 25-minute Python fundamentals assessment.

---

# 10. Wednesday Independent Challenge — No AI

**Duration:** 20–25 minutes

## Problem

Students receive a partially implemented planar robot simulator.

The simulator contains the necessary class structure and plotting utilities.

Their job is to complete selected missing functionality.

## Required Tasks

1. Complete a method that updates the Robot's pose using its motion model.
2. Use a `for` loop to iterate through a list of waypoints.
3. Use a `while` loop to simulate motion toward each waypoint until the robot is within a specified tolerance.
4. Use a conditional statement to determine whether a waypoint has been reached.
5. Store robot positions during simulation.
6. Run the program and plot the resulting trajectory.
7. Explain which objects are composed inside other objects.

Use a supplied controller so students focus on Python fundamentals rather than controller design.

Include a maximum number of simulation steps per waypoint to avoid infinite loops.

The simulator must produce clear output showing whether the robot reached each waypoint.

## Additional Conceptual Questions

Students should briefly answer:

1. What is the difference between a class and an object?
2. What does `self` represent?
3. Why does `Robot` contain a `MotionModel`?
4. What does `return` do inside a method?
5. What is the difference between a `for` loop and a `while` loop?
6. What is the difference between composition and inheritance?

These questions should support assessment, not consume most of the programming time.

## Optional Stretch Challenge

Students who finish early may:

- Swap a HolonomicModel for a UnicycleModel.
- Compare the resulting trajectories.
- Explain why the same waypoint-following controller may not be suitable for both models.
- Add a second Robot object to the Simulator.

Do not require these tasks from every student.

---

# 11. File and Project Structure

Generate an organized teaching repository.

Use approximately the following structure:

```text
robotics_python_workshop/
│
├── README.md
├── requirements.txt
├── python_quick_reference.md
│
├── lecture_01/
│   ├── lecture_01_python_rotations.ipynb
│   └── instructor/
│       └── lecture_01_solutions.ipynb
│
├── lecture_02/
│   ├── main.py
│   ├── pose.py
│   ├── motion_models.py
│   ├── robot.py
│   ├── simulator.py
│   ├── controller.py
│   ├── plotting.py
│   │
│   └── instructor/
│       └── solutions/
│           ├── main.py
│           ├── pose.py
│           ├── motion_models.py
│           ├── robot.py
│           └── simulator.py
│
└── tests/
    ├── test_rotation.py
    └── test_simulator.py
```

The student project must be straightforward to run from the repository root.

Keep imports simple and consistent. Avoid packaging complexity.

If distributing all the lecture materials together, keep instructor solutions clearly separated from student materials so they are not accidentally given to students.

## README Requirements

Include:

- Workshop purpose.
- Prerequisites.
- Environment setup.
- Installing dependencies.
- Opening the notebook in VS Code.
- Running Python scripts in VS Code.
- How to run the simulator.
- How to run tests.
- Lecture-by-lecture instructions.
- Instructor teaching notes.
- Expected output.
- Troubleshooting common setup issues.

Use minimal dependencies, preferably only NumPy, Matplotlib, Jupyter/ipykernel, and pytest.

Do not require ROS, ArduPilot, Gazebo, Docker, or external robotics software.

---

# 12. Instructor and Student Materials

Generate separate instructor and student versions where needed.

## Student Materials

Student-facing materials should contain:

- Concise explanations.
- Runnable demonstrations.
- Partially completed code.
- Clear TODO comments.
- Expected behavior.
- Small checkpoint questions.
- Independent exercises.

Do not provide answers to the independent challenges.

## Instructor Materials

Instructor-facing materials should contain:

- Complete solutions.
- Teaching notes.
- Suggested explanations.
- Expected outputs.
- Likely student misconceptions.
- Common errors.
- Questions to ask during live coding.
- Suggested debugging demonstrations.
- Timing guidance.

Include example questions such as:

- What happens if we forget to return a value?
- What happens if the loop condition is always true?
- Why does NumPy expect radians?
- Why is matrix multiplication different from elementwise multiplication?
- What happens if two objects share the same mutable Pose2D instance?
- Which class is responsible for updating the pose?
- What changes if we replace the motion model?

Demonstrate debugging tools such as breakpoints, stepping through code, and inspecting variables.

---

# 13. Programming Style Guidelines

Assume students are beginners.

Use:

- Descriptive variable names.
- Short methods.
- Explicit intermediate calculations.
- Straightforward control flow.
- Consistent naming.
- Comments explaining mathematical reasoning.
- Minimal dependencies.

Avoid:

- Overly clever Python expressions.
- Dense NumPy broadcasting.
- Complicated comprehensions.
- Decorators.
- Metaclasses.
- Multiple inheritance.
- Complex type systems.
- Unnecessary design patterns.
- Excessive boilerplate.
- Large monolithic classes.
- Unexplained helper abstractions.

Introduce concepts progressively.

Do not require students to understand code that has not yet been explained.

The number of classes should be sufficient to teach composition and inheritance, but their implementations should remain small.

---

# 14. Verification and Testing

Implement and run tests for the mathematical and software components.

At minimum, verify:

### Rotation Matrix

- Zero rotation produces the identity matrix.
- 90° rotation correctly transforms the positive X-axis to the positive Y-axis.
- Rotation preserves vector magnitude.
- Rotation matrices are orthogonal.
- Inverse rotation correctly recovers the original vector.

### Motion Models

- Zero velocity results in no position change.
- A robot with zero yaw moves along world X for positive forward velocity.
- A robot with 90° yaw moves along world Y for positive forward velocity.
- Holonomic lateral velocity is correctly transformed.
- Unicycle lateral velocity is constrained to zero.
- Yaw changes correctly according to commanded yaw rate.

### Simulator

- Multiple time steps update the robot position.
- Trajectory history is recorded correctly.
- The simulation terminates.
- The waypoint-following example reaches its expected targets within tolerance.
- Maximum step limits prevent infinite loops.

Tests should use reasonable floating-point tolerances.

## Student Starter Code Verification

Ensure student starter files remain syntactically valid and importable even where TODO implementations are incomplete.

A TODO should not accidentally prevent the rest of the demonstration from running.

Tests for incomplete student functions may initially fail, but those failures should be intentional and clearly documented.

Verify the completed instructor solution separately.

For notebooks, ensure all cells execute successfully in order after restarting the kernel.

---

# 15. Independent Assessment Philosophy

The final 20–25 minutes of each lecture are intended to evaluate whether students can independently apply concepts taught in class.

Do not make the exercises dependent on memorization of syntax.

Students may consult:

- Lecture notes.
- The Python quick-reference sheet.
- Official documentation.
- Previously demonstrated examples.

Students may not use:

- Codex.
- ChatGPT.
- AI autocomplete that generates solutions.
- Other AI code-generation tools.

These are short in-class exercises, not new homework assignments.

Provide clear completion criteria so students can demonstrate successful execution and briefly explain their work before leaving.

Do not frame the exercises as punitive. The objective is to develop independent engineering capability.

---

# 16. Final Deliverables and Quality Expectations

Generate the complete working repository, not merely a lesson outline.

The materials should allow an instructor to deliver both lectures with minimal additional preparation.

Before finishing:

1. Create a concise overview of the lesson sequence.
2. Implement all student notebooks and scripts.
3. Implement separate instructor solutions.
4. Generate the quick-reference sheet.
5. Generate class diagrams and useful visuals.
6. Execute the completed examples.
7. Run the automated tests.
8. Verify notebook cell execution order.
9. Ensure all examples use consistent coordinate conventions.
10. Confirm the independent exercises are realistic for 20–25 minutes.

Also create a concise instructor checklist covering what to demonstrate, what students should implement, and what they should understand by the end of each lecture.

**Most important design principle:**

The goal is not for students to produce sophisticated software. It is for students to understand how basic Python concepts work together to solve a meaningful robotics problem.

By Wednesday, students should be able to examine their simulator and explain:

- What each file does.
- What each class represents.
- Which objects contain other objects.
- Which classes inherit from others.
- How functions and methods are called.
- How loops advance the simulation.
- How rotation matrices transform robot velocities.
- How the robot's state changes over time.
- How to debug and modify the program independently.

Keep the workshop achievable for students with little Python experience, while still demonstrating software engineering concepts used in real robotics systems.

**Implement the files and validate the completed workshop. Do not stop after proposing the plan.**