# polylalia

Polylalia is an experiment exploring the ability of [stylometric
analysis](https://en.wikipedia.org/wiki/Stylometry) of a body of text.
Polylalia attempts anonymity by running a body of text through the
Yandex translation engine multiple times, ending up with a similar yet
somewhat stilted result.

Think of Polylalia as a script that makes Yandex play [Chinese
whispers](https://en.wikipedia.org/wiki/Chinese_whispers)
with itself and gives you the result. Polylalia only works on plaintext
and is modular, so you can `import polylalia` and use the `Polylalia`
class in your own programs.


### Do not use to protect life or property

This is a basic tool for some research I am doing on stylometric
fingerprinting and authorship with the tools provided by [Drexel
University's PSAL](https://psal.cs.drexel.edu/index.php/Main_Page). It
is meant to prove or disprove a hypothesis that its stylometric
techniques are possibly circumventable by readily accessible scripts.


It has not been audited to provide privacy or anonymity of any kind from
a stylometric analysis. Also, understand that your raw text is being sent
to Yandex, and that you trust Yandex. A user with access to the Yandex
logs could fingerprint this script's behavior.

When I have results of it against the stylometry of PSAL et al I will
update this document.


### Setup/installation

You will need a dependency on
[yandex.translate](https://github.com/tyrannosaurus/python-yandex-translate),
also a free Yandex Translate API key which you can get from [Yandex developer
site](https://tech.yandex.com/).

```
# apt-get install -y python-pip
# pip install -r requirements.txt
```

### Usage

For command-line use, see `./polylalia.py -h`.


### License

GNU GPL V3. See `LICENSE`.


### Donate

If you like Polylalia and are interested in stylometry, donate your time
by teaching others about the importance of free speech and privacy in
your community.
