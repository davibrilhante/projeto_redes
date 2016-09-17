#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stdlib.h>
#include <math.h>

using namespace std;

#define pi 3.14159265;

class Node{
  int n_beams;
  int x, y;
  int radius;

  public: void set(int);
  public: void set_pos(int, int);
  public: void set_radius(int);
  public: double apperture(void)
  {
    return (2*pi/n_beams);
  }
  public: int is_inside(int, int);
};

void Node::set(int n)
{
  n_beams = n;
}

void Node::set(int n)
{
  n_beams = n;
}

void Node::set_radius(int r)
{
  radius = r;
}

public: int is_inside(int a, int b)
{
  double coord_x, coord_y;
  double dist;
  double m;

  dist = hypot(abs(x-a), abs(y-b));

  if(dist <= Radius)
  {
    return 1;
  }
  else
    return 0;

}

int main (int argc, char **argv)
{
  Node node_1;
  node_1.set(4);
  node_1.set_pos(0,0);
  cout <<node_1.apperture(1)<<endl;
  cout<<node_1.is_inside(2, 2)<<endl;
  return 0;
}
