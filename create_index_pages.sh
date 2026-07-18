#!/bin/bash

DOCS="/c/Users/Henry/Documents/Github/tenniskb/docs"

# Foundation Basics EN
cat > "$DOCS/en/foundation/basics/index.md" << 'EOF'
---
title: Foundation Basics
description: Core techniques and quick-reference guides for tennis fundamentals.
---

# Foundation Basics

This section contains foundational tennis content focused on basics — grip, forehand, backhand, footwork, serve, and volley.

## Topics in This Section

<ul>
  <li><a href="Continental%20Grip/index.html">Continental Grip</a></li>
  <li><a href="Forehand%20L-Angle%20and%20Late%20Acceleration/index.html">Forehand L-Angle</a></li>
  <li><a href="Footwork-The-Art-of-Smart-Movement/index.html">Footwork</a></li>
  <li><a href="Backhand-The-Mirror-The-Whip-The-Slice/index.html">Backhand Series</a></li>
  <li><a href="Lob-and-Overhead-Coaching-Guide/index.html">Lob & Overhead</a></li>
  <li><a href="Racket%20Embodiment/index.html">Racket Embodiment</a></li>
</ul>

[← Back to Foundation](../index.html) | [← Back to English Home](../../index.html)
EOF

echo "Created en/foundation/basics/index.md"