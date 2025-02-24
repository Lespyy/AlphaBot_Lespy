import turtle
import time

class AlphaBot:
    def __init__(self):
        # Initialize turtle screen and robot
        self.screen = turtle.Screen()
        self.screen.title("AlphaBot Simulation")
        self.screen.bgcolor("white")
        self.screen.setup(width=600, height=600)

        # Create turtle for the robot
        self.robot = turtle.Turtle()
        self.robot.shape("triangle")
        self.robot.color("blue")
        self.robot.penup()
        self.robot.speed(0)  # Max speed for turtle movements

        # Initial robot state
        self.left_speed = 0
        self.right_speed = 0

    def _update_position(self):
        """
        Update the robot's position and heading based on motor speeds.
        """
        # Calculate turn angle and movement distance
        turn_angle = (self.right_speed - self.left_speed) * 0.5
        move_distance = (self.right_speed + self.left_speed) * 0.05

        # Rotate and move the robot
        self.robot.setheading(self.robot.heading() + turn_angle)
        self.robot.forward(move_distance)

    def setMotor(self, left, right):
        """
        Simulate setting motor speeds.
        """
        self.left_speed = left
        self.right_speed = right
        self._update_position()
        print(f"[SIMULATION] Left motor: {left}, Right motor: {right}")

    def stop(self):
        """
        Stop the robot.
        """
        self.left_speed = 0
        self.right_speed = 0
        print("[SIMULATION] Motors stopped.")

    def __del__(self):
        """
        Clean up the turtle graphics on object deletion.
        """
        self.screen.bye()

if __name__ == "__main__":
    bot = AlphaBot()
    bot.setMotor(50, 50)
    time.sleep(2)
    bot.setMotor(0, 50)
    time.sleep(2)
    bot.stop()
