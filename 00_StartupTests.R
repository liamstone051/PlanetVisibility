library(photobiology)
library(lubridate)
library(astroFns)

dec_form(4, 40, 07)

dec_form <- function(ra_h, ra_m, ra_s) {
  if(ra_h >= 0) {
    result <- ra_h + (ra_m/60) + (ra_s/3600)
  }
  if(ra_h < 0) {
    result <- ra_h - (ra_m/60) - (ra_s/3600)
  }
  result
}

hour_angle <- function(local_s_time, ra_deg) {
  lha <- local_s_time - ra_deg
  if(lha < 0) {
    lha <- lha + 24
  }
  print(lha)
  lha * 15
}

alt <- function(dec, lat, H) {
  asin(sin(lat*(pi/180)) * sin(dec*(pi/180)) + cos(lat*(pi/180)) * cos(dec*(pi/180)) * cos(H*(pi/180)))
}

visibility <- function(ra_h, ra_m, ra_s, dec_h, dec_m, dec_s, obs_long, 
                       obs_lat) {
  ra_deg <- dec_form(ra_h, ra_m, ra_s)
  dec_deg <- dec_form(dec_h, dec_m, dec_s)
  
  local_sidereal_time <- ut2lst(Sys.time(), lon.obs = obs_long)
  local_sidereal_time <- format(local_sidereal_time, format="%Y")
  local_sidereal_time <- as.numeric(local_sidereal_time)
  
  H <- hour_angle(local_sidereal_time, ra_deg)

  altitude <- alt(dec_deg, obs_lat, H)
  print(altitude * (180/pi))
}

visibility(4, 40, 07, 21, 38, 31, 172.569395, -43.538842)



library(globe4r)
create_globe() %>% 
  globe_pov(-21, 179) %>% # position camera
  globe_bars(
    coords(latitude, longitude), 
    data = visibility
  )
