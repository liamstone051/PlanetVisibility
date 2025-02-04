library(sf)
library(mapview)

source("00_StartupTests.R")
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
visibility_circle_sf <- visibility_circle %>%
  st_as_sf(
    coords = c("lon", "lat"),
    crs = 'wgs'
  )
mapview(visibility_circle_sf,
        )
