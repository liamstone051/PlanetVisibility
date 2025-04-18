library(photobiology)
library(lubridate)
library(astroFns)
library(httr)
library(jsonlite)
library(swephR)
library(reticulate)

#reticulate::py_install("skyfield") # Uncomment to install skyfield
skyfield <- import("skyfield.api")

planets <- skyfield$load("de440s.bsp")


dec_form <- function(ra_h, ra_m, ra_s) {
  if(ra_h >= 0) {
    result <- ra_h + (ra_m/60) + (ra_s/3600)
  }
  if(ra_h < 0) {
    result <- ra_h - (ra_m/60) - (ra_s/3600)
  }
  result
}

time_to_long <- function(lst_deg, gst_deg) {
  calc_long <- lst_deg - gst_deg
  if(calc_long > 180) {
    calc_long <- calc_long - 360
  }
  if(calc_long < -180) {
    calc_long <- calc_long + 360
  }
  calc_long * 15
}

hour_angle <- function(local_s_time, ra_deg) {
  lha <- local_s_time - ra_deg
  if(lha < 0) {
    lha <- lha + 24
  }
  lha * 15
}

alt <- function(dec, lat, H) {
  asin(sin(lat*(pi/180)) * sin(dec*(pi/180)) + cos(lat*(pi/180)) * cos(dec*(pi/180)) * cos(H*(pi/180)))
}

visibility <- function(which_planet, obs_long, obs_lat) {
  ts <- skyfield$load$timescale()
  t <- ts$now()
  planet <- planets[which_planet]
  earth <- planets['earth']
  astrometric <- earth$at(t)$observe(planet)
  coords <- astrometric$radec()
  ra_deg <- coords[[1]]
  dec_deg <- coords[[2]]
  ra_deg <- ra_deg$hours
  dec_deg <- dec_deg$degrees
  
  local_sidereal_time <- ut2lst(Sys.time(), lon.obs = obs_long)
  local_sidereal_time <- format(local_sidereal_time, format="%Y")
  local_sidereal_time <- as.numeric(local_sidereal_time)
  greenwich_sidereal_time <- ut2lst(Sys.time(), lon.obs = 0)
  greenwich_sidereal_time <- format(greenwich_sidereal_time, format="%Y")
  greenwich_sidereal_time <- as.numeric(greenwich_sidereal_time)
  
  gst_deg <- greenwich_sidereal_time
  
  calculated_long <- time_to_long(ra_deg, gst_deg)
  print(calculated_long)
  print(dec_deg)
  
  H <- hour_angle(local_sidereal_time, ra_deg)
  
  altitude <- alt(dec_deg, obs_lat, H)
  print(altitude * (180/pi))
}

#visibility('mars barycenter', -92.47437, 26.21957)

zenith_locater <- function(which_planet) {
  ts <- skyfield$load$timescale()
  t <- ts$now()
  planet <- planets[which_planet]
  earth <- planets['earth']
  astrometric <- earth$at(t)$observe(planet)
  coords <- astrometric$radec()
  ra_deg <- coords[[1]]
  dec_deg <- coords[[2]]
  ra_deg <- ra_deg$hours
  dec_deg <- dec_deg$degrees
  
  greenwich_sidereal_time <- ut2lst(Sys.time(), lon.obs = 0)
  greenwich_sidereal_time <- format(greenwich_sidereal_time, format="%Y")
  greenwich_sidereal_time <- as.numeric(greenwich_sidereal_time)
  gst_deg <- greenwich_sidereal_time
  
  calculated_long <- time_to_long(ra_deg, gst_deg)
  
  zenith_coords <- c(dec_deg, calculated_long)
  zenith_coords
}