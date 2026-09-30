#!/bin/sh
# Download FLASH product photos from the Shopify CDN into img/ (needs cdn.shopify.com allowed).
cd "$(dirname "$0")/img" || exit 1
B=https://cdn.shopify.com/s/files/1/0600/1629/6074/files
for f in Flashgray_01 Flashgray_02 Flashgray_03 Flashgray_05 Flashblack_02 Flashblack_03 Flashblack_04 Flashblack01 \
  0E4B5552_5ce51173-6f95-456e-bedd-fd29fbeec615 0E4B5553_e00cba72-d0e8-4dbf-96f8-71074120d149 \
  0E4B5555_ef34294a-7ff7-4a92-baf4-bbc19a21b280 0E4B5557_e89c15e6-0474-4571-a56b-51c49ae6a0ae; do
  curl -sSfo "$f.webp" "$B/$f.webp" || echo "FAILED $f"
done
