#define _USE_MATH_DEFINES
#include <GL/glut.h>
#include <math.h>
#include <stdlib.h>
#include <vector>

// Debug console output
#include <iostream>
using namespace std;

// Define screen size
//int height = 400;
//int width = 400;

// Define the number of circles
int NUM_CIRCLES = 2000;

struct Circle{
    int id;
    float pos_x;
    float pos_y;
    double radius;
    int sides;
    float colour[3];
    double main_vel[2];
    // Constructor
    Circle(int _id=1, float _pos_x=0.2, float _pos_y=0.2, 
           double _radius=0.01, int _sides = 4){
        id = _id;
        pos_x = _pos_x;
        pos_y = _pos_y;
        radius = _radius;
        sides = _sides;
    }
    
    // Draw circle on the screen
    void draw(void){
        //cout << height << endl;
        double theta = 2*M_PI;
        double theta_ = theta/sides;
        double t_x,t_y;  // Top triangle vertex position
        double b_x,b_y; // Bottom triangle vertex position
        
        // I feel like a badass for using MaThS to draw a circle :o
        // This can get very slow when I add lots of circles. 
        // Next iteration will use a buffer to render all of 
        //  the particles in one go
        glPushMatrix(); 
        glTranslatef(pos_x, pos_y, 0.0f);
        for(int i=0;i<sides;i++){
            glBegin(GL_TRIANGLES);
            glVertex2f(0,0);
            t_x = radius*cos((i+1)*theta_);
            t_y = radius*sin((i+1)*theta_);
            b_x = radius*cos(i*theta_);
            b_y = radius*sin(i*theta_);
            
            glColor3f(colour[0], colour[1], colour[2]);
            glVertex2f(b_x,b_y);
            glVertex2f(t_x,t_y);
            glEnd();
        }
        glPopMatrix();
    }
    
};

struct Window{
    int num_circles;
    
    // Array of circle objects
    vector<Circle> circles;
    
    // Constructor
    Window(int _num_circles = 1){
        //cout << "hi\n";
        num_circles = _num_circles;
        for(int i=0;i<num_circles;i++){
            circles.push_back(Circle());
        }
        gen_circles();
    }
    
    // Initialise circles
    void gen_circles(void){
        
        bool gray = false;
        for(int i=0;i<num_circles;i++){
            // Set the RGB colour
            if(gray){
                float rnd_col = rand_val(0.0f,1.0f);
                circles[i].colour[0] = rnd_col;
                circles[i].colour[1] = rnd_col;
                circles[i].colour[2] = rnd_col;
            }else{
                circles[i].colour[0] = rand_val(0.0f,1.0f);//rnd_col;
                circles[i].colour[1] = rand_val(0.0f,1.0f);//rnd_col;
                circles[i].colour[2] = rand_val(0.0f,1.0f);//rnd_col;
            }

            // Set the initial position
            circles[i].pos_x = rand_val(-1.0,1.0);
            //circles[i].pos_x = 0.25f;
            circles[i].pos_y = rand_val(-1.0,1.0);
            // Set the radius
            circles[i].radius = rand_val(0.004f,0.01f);
            if(circles[i].radius > 0.005){
                circles[i].sides = 6;
            }
            // Set the main velocity
            circles[i].main_vel[0] = rand_val(-0.015f,0.015f);
            circles[i].main_vel[1] = rand_val(-0.001,-0.01);
            
            
        }
    }
    
    // Helper function to generate random float
    float rand_val(float min, float max){
        return ((float(rand()) / float(RAND_MAX)) * (max - min)) + min;
    }
    
    // Draw ALL circles
    void draw_circles(void){
        for(int i=0;i<num_circles;i++){
            circles[i].draw();
            //cout << circles[i].pos_x << " " << circles[i].pos_y << endl;
            //cout << circles[i].radius<< endl;
        }
    }
    
    // Simply move all of the particles down
    void move_all(void){
        for(int i=0;i<num_circles;i++){
            circles[i].pos_y -= (0.005 - circles[i].main_vel[1]);
        }
    }
    
    // Calculate physics
    void calc_physics(void){
        for(int i=0;i<num_circles;i++){
            circles[i].pos_y -= 0.35*(0.005 - circles[i].main_vel[1]);
            circles[i].pos_x -= 0.05*(0.005 - circles[i].main_vel[0]);
            if(circles[i].pos_y < -1){
                circles[i].pos_y = 1;
            }
            
            if(circles[i].pos_x < -1){
                circles[i].pos_x = 1;
            }
            if(circles[i].pos_x > 1){
                circles[i].pos_x = -1;
            }
        }
    }
};


Window W(NUM_CIRCLES);

void drawFrame(void)
{
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode(GL_MODELVIEW); 
    W.draw_circles();
    glFlush();
    glutSwapBuffers(); // Swap the buffer
    W.calc_physics(); // Do physics
}

/* Initialize OpenGL Graphics */
void initGL() {
    // Set "clearing" or background color
    glClearColor(0.0f, 0.0f, 0.0f, 1.0f); // Black and opaque
}

/* Called back when there is no other event to be handled */
void idle() {
    glutPostRedisplay();   // Post a re-paint request to activate display()
}

/* Handler for window re-size event. Called back when the window first appears and
 whenever the window is re-sized with its new width and height */
void reshape(GLsizei width, GLsizei height) {  // GLsizei for non-negative integer
    // Compute aspect ratio of the new window
    if (height == 0) height = 1;                // To prevent divide by 0
    GLfloat aspect = (GLfloat)width / (GLfloat)height;
    
    // Set the viewport to cover the new window
    glViewport(0, 0, width, height);
    
    // Set the aspect ratio of the clipping area to match the viewport
    glMatrixMode(GL_PROJECTION);  // To operate on the Projection matrix
    glLoadIdentity();             // Reset the projection matrix
    if (width >= height) {
        // aspect >= 1, set the height from -1 to 1, with larger width
        gluOrtho2D(-1.0 * aspect, 1.0 * aspect, -1.0, 1.0);
    } else {
        // aspect < 1, set the width to -1 to 1, with larger height
        gluOrtho2D(-1.0, 1.0, -1.0 / aspect, 1.0 / aspect);
    }
}

int main(int argc, char** argv)
{
    //static Circle circles[5];
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE);
    glutInitWindowSize(600, 600);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Snow");
    glLoadIdentity();
    glutDisplayFunc(drawFrame);
    //glutReshapeFunc(reshape);
    glutIdleFunc(idle);
    initGL();
    glutMainLoop();
    return 0;
}
