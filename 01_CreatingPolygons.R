library(sf)
library(mapview)
library(geosphere)
library(globe4r)
library(tidyverse)
library(geojsonsf)
library(leaflet)

source("00_StartupTests.R")

center_coords <- zenith_locater('jupiter barycenter')
center_coords

center_lat <- center_coords[1]
center_lon <- center_coords[2]
center_coords
circle_lat <- vector('list', 32)
circle_lon <- vector('list', 32)

for (x in 1:32) {
  new_lat <- 90 * cos(x) + center_lat
  if(new_lat > 90) {
    new_lat <- new_lat - 180
  }
  if(new_lat < -90) {
    new_lat <- new_lat + 180
  }
  circle_lat[[x]] <- new_lat
}

for (x in 1:32) {
  new_lon <- 90 * sin(x) + center_lon
  if(new_lon > 180) {
    new_lon <- new_lon - 360
  }
  if(new_lon < -180) {
    new_lon <- new_lon + 360
  }
  circle_lon[[x]] <- new_lon
}

visibility_circle <- do.call(rbind, Map(data.frame, lat = circle_lat, lon = circle_lon))

earth_radius <- 6371000  # in meters
distance_m <- earth_radius * (pi/2)
bearings_deg <- seq(0, 360 - 360/64, length.out = 64)

circle_points <- destPoint(rlist::list.reverse(center_coords), bearings_deg, distance_m)
circle_points <- as.data.frame(circle_points)
circle_points <- circle_points %>%
  arrange(lon)

if (center_lat >= 0) {
  circle_points <- rbind(c(-180, 90), circle_points)
  circle_points[nrow(circle_points) + 1,] = c(180, 90)
} else {
  circle_points <- rbind(c(-180, -90), circle_points)
  circle_points[nrow(circle_points) + 1,] = c(180, -90)
}
circle_points <- rbind(circle_points, circle_points[1, ])

circle_points_sf <- circle_points %>%
  st_as_sf(
    coords = c("lon", "lat"),
    crs = "wgs84"
  )

circle_polygon_sf <- circle_points %>%
  st_as_sf(
    coords = c("lon", "lat"),
    crs = "wgs84"
  ) %>%
  summarise(geometry = st_combine(geometry)) %>%
  st_cast("POLYGON") 
circle_polygon_sf <- st_polygon(list(as.matrix(circle_points))) |> st_sfc(crs = 4326)


mapview(circle_polygon_sf)
leaflet() %>%
  addTiles() %>%
  addCircleMarkers(data = circle_points_sf)
