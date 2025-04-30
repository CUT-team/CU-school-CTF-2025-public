package godisgopher

func Main() {
	var (
		me  Thing = NewLoveable("Me", 0, true, -1, false)
		you Thing = NewLoveable("You", 0, false, -1, false)
	)

	w := NewWorld(5)
	w.AddThing(&me)
	w.AddThing(&you)
	w.StartSimulation()

	if ps, ok := me.(*PointSet); ok {
		you.AddAttribute(
			ps.GetDimensions().ToAttribute())
	}

	if c, ok := me.(*Circle); ok {
		you.AddAttribute(
			c.GetCircumference().ToAttribute())
	}

	if sw, ok := me.(*SineWave); ok {
		you.AddAction(
			"sit", sw.GetTangent(you.GetXPosition()))
	}

	if seq, ok := me.(*Sequence); ok {
		limit := you.ToLimit()
		seq.SetLimit(limit)
	}

	me.ToggleCurrent()

	me.CanSee(false)
	me.AddFeeling("dizzy")

	w.TimeTravelForTwo("AD", 617, &me, &you)
	w.TimeTravelForTwo("BC", 3691, &me, &you)

	w.Unite(&me, &you)

	if me.GetSimulationsAvailable() >= you.GetSimulationsNeeded() {
		you.SetSatisfaction(
			me.ToSatisfaction())
	}

	if you.GetFeelingIndex("happy") != -1 {
		me.RequestExecution(w)
	}

	w.LockThing(&me)
	w.LockThing(&you)

	if ep, ok := me.(*Eggplant); ok {
		you.AddAttribute(
			ep.GetNutrients().ToAttribute())
		ep.ResetNutrients()
	}
	if t, ok := me.(*Tomato); ok {
		you.AddAttribute(
			t.GetAntioxidants().ToAttribute())
		t.ResetAntioxidants()
	}
	if tc, ok := me.(*TabbyCat); ok {
		tc.Purr()
	}

	if *w.GetGod() == me {
		me.SetProof(
			you.ToProof())
	}

	me.ToggleGender()
	w.Procreate(&me, &you)
	me.ToggleRole()
	w.MakeHigh(&me)
	w.MakeHigh(&you)

	if me.GetSenseIndex("vibration") != -1 {
		me.AddFeeling("complete")
	}
	w.Unlock(&you)
	w.RemoveThing(&you)
	for range 5 {
		me.LookFor(&you, w)
	}

	if me.GetMemory().IsErasable() {
		me.RemoveFeeling("disheartened")
	}

	if err := me.SetOpinion(
		me.GetOpinionIndex("you are here"), false); err != nil {
		w.Announce("God is always true.")
	}

	for range 12 {
		w.RunExecution()
	}

	langs := map[string]string{
		"1": "de",
		"2": "es",
		"3": "fr",
		"4": "kr",
		"5": "se",
		"6": "cn",
	}
	for i, lang := range langs {
		w.Announce(i, lang)
	}
	w.RunExecution()

	if w.IsExecutableBy(&me) {
		exe := me.ToExecution()
		you.SetExecution(exe)
	}

	if w.GetThingIndex(&you) != -1 {
		w.RunExecution()
	}
	me.Escape(w)

	end := "love"
	me.LearnTopic(end)
	me.TakeExamTopic(end)
	me.GetAlgebraicExpression(end)
	me.Escape(end)

	w.Execute(&me)
}
