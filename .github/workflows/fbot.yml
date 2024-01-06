name: fbot
on:
  workflow_dispatch:
jobs:
  run-sync-service:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository code
        uses: actions/checkout@v2
      - name: Cd Into Repo
        run: |
          cd ${{ github.workspace }}
      - name: Running the Script 
        run: |
          sudo bash startup.sh
      - name: Running the Script 
        run: |
          sudo python fbot.py
