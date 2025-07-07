import {
    Astronomy,
    Body              // enum of solar‑system bodies
  } from 'https://cdn.jsdelivr.net/npm/astronomy-engine@2.1.0/dist/esm/astronomy.module.js';

  /* ---------- helpers ---------- */

  // Convert "Local Sidereal Time – Greenwich Sidereal Time" into longitude (deg)
  // Inputs are in *hours* because astronomy‐engine already gives RA and GST in hours.
  function timeToLong(lstHours, gstHours) {
    let diff = lstHours - gstHours;     // hours
    if (diff > 12)  diff -= 24;         // wrap into ±12 h range
    if (diff < -12) diff += 24;
    return diff * 15;                   // 15 deg per sidereal hour
  }

  /**
   * Return the sub‑planet point (lat/lon) for any solar‑system body
   * @param {string} planetName  e.g. "Mars", "Jupiter", "Moon", "Pluto"
   * @returns {{lat:number, lon:number}}  degrees, WGS‑84
   */
  function zenithLocator(planetName) {

    // 1) Time of the computation
    const now = new Date();               // UTC by default

    // 2) RA/Dec of the body referred to the *true equator of date*
    const equ = Astronomy.Equator(
      Body[planetName],                   // astronomy‑engine enum value
      now,
      'equator',                          // use the true equator, not the ecliptic
      'ofDate'                            // epoch-of-date coordinates
    );

    // 3) Greenwich (apparent) sidereal time, in hours
    const gstHours = Astronomy.SiderealTime(now);   // 0‥24 h

    // 4) Convert RA & GST to sub‑point longitude
    const lonDeg = timeToLong(equ.ra, gstHours);

    // 5) Sub‑point latitude is just the body’s apparent declination
    const latDeg = equ.dec;

    return { lat: latDeg, lon: lonDeg };
  }

  /* ---------- demo ---------- */

  console.log('Sub‑Mars point right now:', zenithLocator('Jupiter'));
  console.log('Sub‑Moon point right now:', zenithLocator('Moon'));