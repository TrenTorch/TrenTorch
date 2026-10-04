---
title: Robotic Arm Inverse Kinematics
name: rl-robotic-arm
difficulty: Advanced
tags: [rl, robotics, continuous-control, inverse-kinematics]
---

## Statement

Control 2D robotic arm to reach target position. State: [joint angles]. Actions: [joint torques]. Reward: -dist(endpoint, target) - action_cost.

### The problem, from first principles

Arm endpoint position is nonlinear function of joint angles. RL must learn inverse kinematics: given target, find joint angles.

### From theory to code

Implement `compute_arm_kinematics(joint_angles, link_lengths)` which:
- Takes joint angles and link lengths
- Computes endpoint position using forward kinematics
- Returns (x, y) position of end-effector

### Constraints

- 2D arm with two joints (DOF=2)
- Link lengths fixed: [L1, L2]
- Actions affect joint angles
- Dense reward based on distance to target

### Hints

<details>
<summary>Hint 1: Forward kinematics</summary>
x = L1*cos(θ1) + L2*cos(θ1+θ2), similar for y
</details>

<details>
<summary>Hint 2: Inverse problem</summary>
Goal: find θ1, θ2 given target (x,y)
</details>

<details>
<summary>Hint 3: Action scaling</summary>
Torques should be integrated to update joint angles
</details>

## Theory

### Arm kinematics

Forward: (θ1, θ2) -> (x, y)
Inverse: (x, y) -> (θ1, θ2) [multiple solutions possible]

### Control

RL learns end-to-end mapping from observation to torques.

## Explanation

Robotics is major RL application. Arms, hands, locomotion all use modern RL techniques.
