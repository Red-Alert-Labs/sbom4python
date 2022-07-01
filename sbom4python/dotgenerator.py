# Copyright (C) 2022 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

VERSION = "0.1"


class DOTGenerator:
    def __init__(self):
        self.dot = []

    def getDOT(self):
        return self.dot

    def show(self, text):
        # print (text)
        self.dot.append(text)

    def get_package(self, package_id):
        # Remove SPDXId from package_id if found in package_id.
        # Expected format is SPDXRef-Package-n-<package>
        prefix = "SPDXRef-Package-"
        if prefix in package_id:
            # Find package name after package number
            startpos = len(prefix) + 1
            return package_id[package_id[startpos:].find("-") + startpos + 1 :]
        return package_id

    def generatedot(self, data):

        # Generate header
        self.show("strict digraph sbom {")
        self.show('\tsize="8,10.5"; ratio=fill;')
        # Generate graph
        root = ""
        explicit_style = " [shape=box, style=filled, fontcolor=white, fillcolor=blue];"
        implicit_style = " [shape=box, style=filled, fontcolor=white, fillcolor=green];"
        packages = []
        for element in data:
            source = element[0]
            dest = element[1]
            relationship = element[2]

            lib = '"' + self.get_package(source) + '"'
            application = '"' + self.get_package(dest) + '"'

            if relationship == " DESCRIBES ":
                # Should only be one DESCRIBES relationship.
                root = application
            else:
                if lib == root:
                    if lib not in packages:
                        packages.append(lib)
                        self.show(
                            "\t" + lib + " [shape=box, style=filled, fillcolor=red];"
                        )
                    if application not in packages:
                        packages.append(application)
                        self.show("\t" + application + explicit_style)
                elif application == root:
                    if lib not in packages:
                        packages.append(lib)
                        self.show("\t" + lib + explicit_style)
                else:
                    if lib not in packages:
                        packages.append(lib)
                        self.show("\t" + lib + implicit_style)
                    if application not in packages:
                        packages.append(application)
                        self.show("\t" + application + implicit_style)
                self.show("\t" + lib + " -> " + application + ";")
        self.show("}")
        # end
