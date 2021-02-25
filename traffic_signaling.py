import numpy as np

print("Developed by Team Zodiac\n Lucas Aranda La Hoz & José Javier Blázquez Campos")

def parsing(filename):
  time_sim = 0
  n_intersections = 0
  n_streets = 0
  n_cars = 0
  values_streets = np.zeros((1,1))

  input_file = open(filename, "r")
  input_array = input_file.read()
  lines_array = input_array.split("\n")

  car_paths = list()
  street_keys = list()

  for index, line in enumerate(lines_array):
    if index == 0:
      values = line.split();
      time_sim = int(values[0])
      n_intersections = int(values[1])
      n_streets = int(values[2])
      n_cars = int(values[3])
      values_streets = np.zeros((n_streets, 3))
    elif index <= n_streets:
      temp_street = line.split()
      street_keys.append(temp_street[2])
      del temp_street[2]
      values_streets[index-1] = np.array(temp_street)
    else:
      car_paths.append((line.split()[1:]))
  return time_sim, n_intersections, n_streets, n_cars, values_streets, car_paths, street_keys


def list_intersections(values_streets, street_keys):
  intersections = dict();
  for index, street in enumerate(values_streets):
      if street[1] in intersections.keys():
        intersections[street[1]][street_keys[index]] = 0
      else:
        intersections[int(street[1])] = dict()
        intersections[street[1]][street_keys[index]] = 0
  return intersections


def weights(n_cars, car_paths, intersections, time_sim, values_streets, street_keys):
  cum_time = 0
  for car in range(1,n_cars):
    for street in reversed(car_paths[car]):
      intersections[(values_streets[street_keys.index(street)][1])][street] += cum_time
      cum_time += values_streets[street_keys.index(street)][2]
    cum_time = 0
  return 0


def trafficlight_timing(intersections):
  for intersection in intersections.items():
    streets = intersection[1]
    sorted_streets = sorted(streets, key=streets.get)
    for i, element in enumerate(sorted_streets):
      intersections[intersection[0]][element] = len(sorted_streets)-int(i)
  return intersections


def unparse(intersections, n_intersections):
  output = str(n_intersections) + "\n"
  for intersection in range(n_intersections):
    output+= str(intersection) + "\n"
    output+= str(len(intersections[intersection])) + "\n"
    for street in intersections[intersection]:
      output+= street + " " + str(intersections[intersection][street]) + "\n"
  return output


def main():
  print("Parsing file")
  time_sim, n_intersections, n_streets, n_cars, values_streets, car_paths, street_keys = parsing("d.txt")
  print("Listing intersections")
  intersections = list_intersections(values_streets, street_keys)
  print("Calculating weight for each intersection")
  weights(n_cars, car_paths, intersections, time_sim, values_streets, street_keys)
  print("Tweaking Traffic Lights")
  intersections = trafficlight_timing(intersections)
  print("Unparse")
  output  = unparse(intersections, n_intersections)
  print("Generate file")
  f = open("d_solution", "a")
  f.write(output)
  f.close()
  return 0


if __name__ == "__main__":
  main()