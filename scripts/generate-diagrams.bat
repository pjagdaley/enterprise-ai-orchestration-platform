@echo off

for /R docs\diagrams %%f in (*.puml) do (
    java -jar tools\plantuml.jar -tsvg "%%f"
)

echo Diagrams generated successfully.