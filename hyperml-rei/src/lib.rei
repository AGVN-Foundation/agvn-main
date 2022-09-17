#*
    HyperML
*#

export trait Stage {
    fn run()
}

data Pipeline {
    stages: Iter<dyn Stage>
}

system Pipeline {
    impl New(stages: dyn Stage...) -> Self { stages.collect() }
}

system Pipeline {
    fn(&mut self) run() {
        stages.next().run()
    }
}
