package godisgopher

type (
	Attribute    interface{}
	Action       interface{}
	Limit        interface{}
	Position     interface{}
	Satisfaction interface{}
	Proof        interface{}
	Execution    interface{}
)

type Memory struct{}

func (m *Memory) IsErasable() bool

type Thing interface {
	AddAttribute(a *Attribute)
	AddAction(actionName string, a ...any)
	SetLimit(l *Limit)
	GetXPosition() float64
	ToLimit() *Limit
	ToggleCurrent()
	CanSee(s bool)
	AddFeeling(feeling string)
	GetSimulationsAvailable() int
	GetSimulationsNeeded() int
	SetSatisfaction(s *Satisfaction)
	ToSatisfaction() *Satisfaction
	GetFeelingIndex(feeling string) int
	RequestExecution(w *World)
	SetProof(p *Proof)
	ToProof() *Proof
	ToggleGender()
	ToggleRole()
	GetSenseIndex(sense string) int
	LookFor(t *Thing, w *World)
	GetMemory() *Memory
	RemoveFeeling(feeling string)
	GetOpinionIndex(opinion string) int
	SetOpinion(opinionIndex int, s bool) error
	SetExecution(e *Execution)
	ToExecution() *Execution
	Escape(target any)
	LearnTopic(topic string)
	TakeExamTopic(topic string)
	GetAlgebraicExpression(query string) string
}

type baseThing struct{}

func (b *baseThing) AddAttribute(a *Attribute)
func (b *baseThing) AddAction(actionName string, a ...any)
func (b *baseThing) SetLimit(l *Limit)
func (b *baseThing) GetXPosition() float64
func (b *baseThing) ToLimit() *Limit
func (b *baseThing) ToggleCurrent()
func (b *baseThing) CanSee(s bool)
func (b *baseThing) AddFeeling(feeling string)
func (b *baseThing) GetSimulationsAvailable() int
func (b *baseThing) GetSimulationsNeeded() int
func (b *baseThing) SetSatisfaction(s *Satisfaction)
func (b *baseThing) ToSatisfaction() *Satisfaction
func (b *baseThing) GetFeelingIndex(feeling string) int
func (b *baseThing) RequestExecution(w *World)
func (b *baseThing) SetProof(p *Proof)
func (b *baseThing) ToProof() *Proof
func (b *baseThing) ToggleGender()
func (b *baseThing) ToggleRole()
func (b *baseThing) GetSenseIndex(sense string) int
func (b *baseThing) LookFor(t *Thing, w *World)
func (b *baseThing) GetMemory() *Memory
func (b *baseThing) RemoveFeeling(feeling string)
func (b *baseThing) GetOpinionIndex(opinion string) int
func (b *baseThing) SetOpinion(opinionIndex int, s bool) error
func (b *baseThing) SetExecution(e *Execution)
func (b *baseThing) ToExecution() *Execution
func (b *baseThing) Escape(target any)
func (b *baseThing) LearnTopic(topic string)
func (b *baseThing) TakeExamTopic(topic string)
func (b *baseThing) GetAlgebraicExpression(query string) string

type Loveable struct {
	baseThing
}

func NewLoveable(name string, initialLove int, isProgram bool, emotionalState int, isComplete bool) *Loveable

type World struct{}

func NewWorld(size int) *World
func (w *World) AddThing(t *Thing)
func (w *World) StartSimulation()
func (w *World) TimeTravelForTwo(era string, year uint, t1, t2 *Thing)
func (w *World) Unite(t1, t2 *Thing)
func (w *World) LockThing(t *Thing)
func (w *World) GetGod() *Thing
func (w *World) Procreate(t1, t2 *Thing)
func (w *World) MakeHigh(t *Thing)
func (w *World) Unlock(t *Thing)
func (w *World) RemoveThing(t *Thing)
func (w *World) Announce(a ...any)
func (w *World) RunExecution()
func (w *World) IsExecutableBy(t *Thing) bool
func (w *World) GetThingIndex(t *Thing) int
func (w *World) Execute(t *Thing)

type Dimensions struct{}

func (d *Dimensions) ToAttribute() *Attribute

type PointSet struct {
	baseThing
}

func (ps *PointSet) GetDimensions() *Dimensions

type Circumference struct{}

func (c *Circumference) ToAttribute() *Attribute

type Circle struct {
	baseThing
}

func (c *Circle) GetCircumference() *Circumference

type Tangent struct{}

type SineWave struct {
	baseThing
}

func (sw *SineWave) GetTangent(x float64) *Tangent

type Sequence struct {
	baseThing
}

type Nutriens struct{}

func (n *Nutriens) ToAttribute() *Attribute

type Eggplant struct {
	baseThing
}

func (ep *Eggplant) GetNutrients() *Nutriens
func (ep *Eggplant) ResetNutrients()

type Antioxidants struct{}

func (a *Antioxidants) ToAttribute() *Attribute

type Tomato struct {
	baseThing
}

func (t *Tomato) GetAntioxidants() *Antioxidants
func (t *Tomato) ResetAntioxidants()

type TabbyCat struct {
	baseThing
}

func (tc *TabbyCat) Purr()
