import React, { useMemo, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from "recharts";
import { motion } from "framer-motion";
import { Orbit, Radar, Sparkles, SlidersHorizontal, FileText } from "lucide-react";

const PLANE_META = {
  p1: {
    title: "Plane 1 · Internal State",
    subtitle: "Perceived Need × Emotional Stability",
    shortFunction: "Diagnoses how psychologically held, needed, and emotionally steady a person feels in a relationship.",
    xLabel: "Perceived Need",
    yLabel: "Emotional Stability",
    xPrompt: "How strongly do you feel needed in this relationship?",
    yPrompt: "How emotionally stable do you feel while staying in this role?",
    quadrants: {
      Q1: {
        name: "Role Fulfillment",
        desc: "You feel needed and emotionally capable of carrying that role. The relationship may feel meaningful and structurally affirming.",
      },
      Q2: {
        name: "Safe but Empty",
        desc: "You feel stable, but your sense of being needed is low. The connection may feel orderly yet lacking vitality or emotional significance.",
      },
      Q3: {
        name: "Self-Worth Fracture",
        desc: "You feel neither securely needed nor internally stable. This often creates insecurity, self-doubt, or emotional withdrawal.",
      },
      Q4: {
        name: "Collapse Risk",
        desc: "You feel highly needed, but emotionally unable to sustain the pressure. This can produce overload, panic, or a hidden sense of collapse.",
      },
    },
  },
  p2: {
    title: "Plane 2 · Power Dynamics",
    subtitle: "How much I need the other × How much I am needed",
    shortFunction: "Maps mutual dependency and the likely distribution of leverage or bargaining power.",
    xLabel: "How much I need the other",
    yLabel: "How much I am needed",
    xPrompt: "How much do you need the other person right now?",
    yPrompt: "How much do you think the other person needs you?",
    quadrants: {
      Q1: {
        name: "Mutual Interdependence",
        desc: "Both attachment and usefulness are relatively high. This tends to feel reciprocal and can support a more resilient bond.",
      },
      Q2: {
        name: "Power Advantage",
        desc: "You are more needed than needy. This often increases your structural leverage and reduces your vulnerability to abrupt loss.",
      },
      Q3: {
        name: "Weak Attachment",
        desc: "Neither side appears deeply dependent. This can feel free and low-pressure, but also thin, replaceable, or hard to consolidate.",
      },
      Q4: {
        name: "Anxious Pursuit",
        desc: "You need the other more than you are needed. This creates asymmetry, often increasing fear, over-investment, or bargaining weakness.",
      },
    },
  },
  p3: {
    title: "Plane 3 · Motivational Structure",
    subtitle: "How much I need the other × Material-to-Emotional Orientation",
    shortFunction: "Identifies whether the relationship is driven more by emotional/ideational attachment or practical/material dependence.",
    xLabel: "How much I need the other",
    yLabel: "Material → Emotional / Ideational",
    xPrompt: "How much do you need this relationship to continue?",
    yPrompt: "Is your need more material/practical or more emotional/ideational?",
    quadrants: {
      Q1: {
        name: "Deep Affective Bond",
        desc: "Need is high and the tie is emotionally or ideationally oriented. The relationship is often experienced as meaningful, intimate, or identity-relevant.",
      },
      Q2: {
        name: "Principled Commitment",
        desc: "Need is lower, but the bond is still guided by values, care, responsibility, or non-material meaning.",
      },
      Q3: {
        name: "Low-Need Reflective Tie",
        desc: "The relationship is not heavily need-based and is not strongly material. It may remain thoughtful, but relatively non-binding.",
      },
      Q4: {
        name: "Pragmatic Dependence",
        desc: "Need is high and materially grounded. The bond may be sustained by practical support, stability, or concrete life resources.",
      },
    },
  },
};

const PRESETS = {
  balanced: { x: 72, y: 72 },
  strained: { x: 82, y: 28 },
  detached: { x: 28, y: 62 },
  fractured: { x: 22, y: 22 },
};

function getQuadrant(x, y) {
  if (x >= 50 && y >= 50) return "Q1";
  if (x < 50 && y >= 50) return "Q2";
  if (x < 50 && y < 50) return "Q3";
  return "Q4";
}

function interpretPlane(planeId, point) {
  const quadrant = getQuadrant(point.x, point.y);
  const meta = PLANE_META[planeId];
  return {
    quadrant,
    ...meta.quadrants[quadrant],
  };
}

function classifyDyad(a, b) {
  const p1Gap = Math.abs(a.p1.x - b.p1.x) + Math.abs(a.p1.y - b.p1.y);
  const p2Gap = Math.abs(a.p2.x - b.p2.x) + Math.abs(a.p2.y - b.p2.y);
  const p3Gap = Math.abs(a.p3.x - b.p3.x) + Math.abs(a.p3.y - b.p3.y);
  const avgGap = Math.round((p1Gap + p2Gap + p3Gap) / 3);

  let structure = "Dynamic but workable";
  if (p2Gap <= 18 && p1Gap <= 20) structure = "Mutual balance";
  else if (a.p2.x >= 65 && a.p2.y <= 45) structure = "A-leaning one-sided dependence";
  else if (b.p2.x >= 65 && b.p2.y <= 45) structure = "B-leaning one-sided dependence";
  else if (p2Gap >= 40) structure = "Power asymmetry risk";
  else if (avgGap <= 22) structure = "Relatively aligned dyad";

  let risk = "Low";
  if (avgGap >= 55) risk = "High";
  else if (avgGap >= 32) risk = "Moderate";

  return { structure, risk, p1Gap, p2Gap, p3Gap, avgGap };
}

function PlaneChart({ planeId, pointA, pointB, dualMode }) {
  const meta = PLANE_META[planeId];
  const data = dualMode
    ? [
        { label: "A", x: pointA.x, y: pointA.y },
        { label: "B", x: pointB.x, y: pointB.y },
      ]
    : [{ label: "You", x: pointA.x, y: pointA.y }];

  return (
    <div className="rounded-3xl border border-slate-200 bg-white/80 p-4 shadow-sm backdrop-blur">
      <div className="mb-3">
        <div className="text-lg font-semibold tracking-tight text-slate-900">{meta.title}</div>
        <div className="text-sm text-slate-500">{meta.subtitle}</div>
        <div className="mt-2 text-sm leading-6 text-slate-600">{meta.shortFunction}</div>
      </div>
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 10, right: 12, bottom: 20, left: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#cbd5e1" />
            <XAxis
              type="number"
              dataKey="x"
              domain={[0, 100]}
              tick={{ fill: "#475569", fontSize: 12 }}
              label={{ value: meta.xLabel, position: "insideBottom", offset: -10, fill: "#475569" }}
            />
            <YAxis
              type="number"
              dataKey="y"
              domain={[0, 100]}
              tick={{ fill: "#475569", fontSize: 12 }}
              label={{ value: meta.yLabel, angle: -90, position: "insideLeft", fill: "#475569" }}
            />
            <ReferenceLine x={50} stroke="#64748b" strokeDasharray="4 4" />
            <ReferenceLine y={50} stroke="#64748b" strokeDasharray="4 4" />
            <Tooltip />
            <Scatter data={data} fill="#1e293b" />
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function GuideControls({ title, xLabel, yLabel, xValue, yValue, onXChange, onYChange }) {
  return (
    <div className="space-y-5 rounded-3xl border border-slate-200 bg-white/80 p-5 shadow-sm backdrop-blur">
      <div className="text-base font-semibold text-slate-900">{title}</div>
      <div className="space-y-2">
        <Label className="text-sm text-slate-700">{xLabel}</Label>
        <div className="flex items-center gap-4">
          <Slider value={[xValue]} min={0} max={100} step={1} onValueChange={onXChange} />
          <div className="w-12 text-right text-sm font-semibold text-slate-700">{xValue}</div>
        </div>
      </div>
      <div className="space-y-2">
        <Label className="text-sm text-slate-700">{yLabel}</Label>
        <div className="flex items-center gap-4">
          <Slider value={[yValue]} min={0} max={100} step={1} onValueChange={onYChange} />
          <div className="w-12 text-right text-sm font-semibold text-slate-700">{yValue}</div>
        </div>
      </div>
    </div>
  );
}

function PersonSection({ label, person, setPerson, dualMode, otherPerson }) {
  const p1 = interpretPlane("p1", person.p1);
  const p2 = interpretPlane("p2", person.p2);
  const p3 = interpretPlane("p3", person.p3);

  const setPlaneValue = (plane, axis, value) => {
    setPerson({
      ...person,
      [plane]: {
        ...person[plane],
        [axis]: value[0],
      },
    });
  };

  return (
    <Card className="rounded-3xl border-0 bg-white/75 shadow-sm backdrop-blur">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-2xl text-slate-900">
          <Orbit className="h-5 w-5" /> {label}
        </CardTitle>
        <CardDescription className="leading-6">
          Start from the planes. Then use guided sliders to refine the point positions and receive immediate interpretation.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <PlaneChart planeId="p1" pointA={person.p1} pointB={otherPerson?.p1} dualMode={dualMode} />

        <div className="grid gap-3 md:grid-cols-3">
          <Badge variant="secondary" className="justify-start rounded-2xl px-4 py-3 text-sm">Plane 1 · {p1.name}</Badge>
          <Badge variant="secondary" className="justify-start rounded-2xl px-4 py-3 text-sm">Plane 2 · {p2.name}</Badge>
          <Badge variant="secondary" className="justify-start rounded-2xl px-4 py-3 text-sm">Plane 3 · {p3.name}</Badge>
        </div>

        <Tabs defaultValue="p1" className="space-y-4">
          <TabsList className="rounded-2xl bg-slate-100">
            <TabsTrigger value="p1">Plane 1</TabsTrigger>
            <TabsTrigger value="p2">Plane 2</TabsTrigger>
            <TabsTrigger value="p3">Plane 3</TabsTrigger>
          </TabsList>

          <TabsContent value="p1" className="space-y-4">
            <GuideControls
              title="Guided adjustment · Plane 1"
              xLabel={PLANE_META.p1.xPrompt}
              yLabel={PLANE_META.p1.yPrompt}
              xValue={person.p1.x}
              yValue={person.p1.y}
              onXChange={(v) => setPlaneValue("p1", "x", v)}
              onYChange={(v) => setPlaneValue("p1", "y", v)}
            />
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
              <div className="text-xs uppercase tracking-[0.18em] text-slate-500">Interpretation</div>
              <div className="mt-2 text-lg font-semibold text-slate-900">{p1.name}</div>
              <div className="mt-2 text-sm leading-6 text-slate-600">{p1.desc}</div>
            </div>
          </TabsContent>

          <TabsContent value="p2" className="space-y-4">
            <GuideControls
              title="Guided adjustment · Plane 2"
              xLabel={PLANE_META.p2.xPrompt}
              yLabel={PLANE_META.p2.yPrompt}
              xValue={person.p2.x}
              yValue={person.p2.y}
              onXChange={(v) => setPlaneValue("p2", "x", v)}
              onYChange={(v) => setPlaneValue("p2", "y", v)}
            />
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
              <div className="text-xs uppercase tracking-[0.18em] text-slate-500">Interpretation</div>
              <div className="mt-2 text-lg font-semibold text-slate-900">{p2.name}</div>
              <div className="mt-2 text-sm leading-6 text-slate-600">{p2.desc}</div>
            </div>
          </TabsContent>

          <TabsContent value="p3" className="space-y-4">
            <GuideControls
              title="Guided adjustment · Plane 3"
              xLabel={PLANE_META.p3.xPrompt}
              yLabel={PLANE_META.p3.yPrompt}
              xValue={person.p3.x}
              yValue={person.p3.y}
              onXChange={(v) => setPlaneValue("p3", "x", v)}
              onYChange={(v) => setPlaneValue("p3", "y", v)}
            />
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
              <div className="text-xs uppercase tracking-[0.18em] text-slate-500">Interpretation</div>
              <div className="mt-2 text-lg font-semibold text-slate-900">{p3.name}</div>
              <div className="mt-2 text-sm leading-6 text-slate-600">{p3.desc}</div>
            </div>
          </TabsContent>
        </Tabs>

        <div className="flex flex-wrap gap-3">
          <Button variant="outline" className="rounded-2xl" onClick={() => setPerson({ ...person, p1: PRESETS.balanced })}>Preset: balanced P1</Button>
          <Button variant="outline" className="rounded-2xl" onClick={() => setPerson({ ...person, p2: PRESETS.strained })}>Preset: strained P2</Button>
          <Button variant="outline" className="rounded-2xl" onClick={() => setPerson({ ...person, p3: PRESETS.detached })}>Preset: detached P3</Button>
        </div>
      </CardContent>
    </Card>
  );
}

export default function APSInteractiveTool() {
  const [dualMode, setDualMode] = useState(true);
  const [notes, setNotes] = useState("");

  const [a, setA] = useState({
    p1: { x: 72, y: 68 },
    p2: { x: 54, y: 60 },
    p3: { x: 61, y: 74 },
  });

  const [b, setB] = useState({
    p1: { x: 42, y: 52 },
    p2: { x: 33, y: 71 },
    p3: { x: 31, y: 46 },
  });

  const aP1 = interpretPlane("p1", a.p1);
  const aP2 = interpretPlane("p2", a.p2);
  const aP3 = interpretPlane("p3", a.p3);
  const bP1 = interpretPlane("p1", b.p1);
  const bP2 = interpretPlane("p2", b.p2);
  const bP3 = interpretPlane("p3", b.p3);

  const dyad = useMemo(() => (dualMode ? classifyDyad(a, b) : null), [a, b, dualMode]);

  const generatedDescription = useMemo(() => {
    if (!dualMode) {
      return `The current positioning suggests that Person A is moving through the relationship with a ${aP1.name.toLowerCase()} internal state, a ${aP2.name.toLowerCase()} power structure, and a ${aP3.name.toLowerCase()} motivational orientation. Together, this suggests a relationship experience shaped more by positional tension than by a simple emotional label.`;
    }

    return `This dyad currently resembles a ${dyad?.structure?.toLowerCase() || "dynamic structure"}. Person A appears to occupy ${aP1.name.toLowerCase()} on the internal plane, ${aP2.name.toLowerCase()} on the power plane, and ${aP3.name.toLowerCase()} on the motivational plane. Person B appears to occupy ${bP1.name.toLowerCase()}, ${bP2.name.toLowerCase()}, and ${bP3.name.toLowerCase()} respectively. The overall mismatch level is ${dyad?.risk?.toLowerCase() || "unclear"}, suggesting that the relationship may be stabilized by some dimensions while strained by others. Rather than reading the relationship as simply secure or insecure, APS treats it as a structured system whose tensions emerge from asymmetry, role load, and motive alignment.`;
  }, [dualMode, aP1, aP2, aP3, bP1, bP2, bP3, dyad]);

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(30,41,59,0.08),_transparent_28%),linear-gradient(180deg,#f8fafc_0%,#eef2ff_100%)] p-6 md:p-10">
      <div className="mx-auto max-w-7xl space-y-6">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="grid gap-4 lg:grid-cols-[1fr_auto] lg:items-end">
          <div>
            <div className="mb-3 flex items-center gap-2 text-sm font-medium uppercase tracking-[0.22em] text-slate-500">
              <Sparkles className="h-4 w-4" /> Affective Positioning System
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-slate-900 md:text-6xl">A designed, plane-first APS prototype</h1>
            <p className="mt-4 max-w-3xl text-base leading-7 text-slate-600 md:text-lg">
              A cleaner APS interface built around the planes themselves. Users can first think spatially, then refine positions with guided sliders, and finally receive a generated structural description.
            </p>
          </div>
          <div className="flex items-center gap-3 rounded-3xl border border-slate-200 bg-white/80 px-4 py-3 shadow-sm backdrop-blur">
            <Switch checked={dualMode} onCheckedChange={setDualMode} id="dual-mode" />
            <Label htmlFor="dual-mode" className="font-medium text-slate-700">Dual-person mode</Label>
          </div>
        </motion.div>

        <div className={`grid gap-6 ${dualMode ? "xl:grid-cols-2" : "xl:grid-cols-1"}`}>
          <PersonSection label="Person A" person={a} setPerson={setA} dualMode={dualMode} otherPerson={b} />
          {dualMode && <PersonSection label="Person B" person={b} setPerson={setB} dualMode={dualMode} otherPerson={a} />}
        </div>

        <Card className="rounded-3xl border-0 bg-white/75 shadow-sm backdrop-blur">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-2xl text-slate-900"><Radar className="h-5 w-5" /> Generated structural report</CardTitle>
            <CardDescription>
              This section synthesizes the current points into a generated description rather than a single score or label.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {dualMode && dyad ? (
              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
                <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4 xl:col-span-2">
                  <div className="text-xs uppercase tracking-[0.18em] text-slate-500">Relationship structure</div>
                  <div className="mt-2 text-xl font-semibold text-slate-900">{dyad.structure}</div>
                  <div className="mt-2 text-sm leading-6 text-slate-600">A compact reading of how the current relationship appears to be organized.</div>
                </div>
                <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                  <div className="text-xs uppercase tracking-[0.18em] text-slate-500">Risk level</div>
                  <div className="mt-2 text-xl font-semibold text-slate-900">{dyad.risk}</div>
                </div>
                <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                  <div className="text-xs uppercase tracking-[0.18em] text-slate-500">Power gap</div>
                  <div className="mt-2 text-xl font-semibold text-slate-900">{dyad.p2Gap}</div>
                </div>
                <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                  <div className="text-xs uppercase tracking-[0.18em] text-slate-500">Motivational gap</div>
                  <div className="mt-2 text-xl font-semibold text-slate-900">{dyad.p3Gap}</div>
                </div>
              </div>
            ) : (
              <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5 text-slate-600">
                Single-person mode emphasizes self-location. Switch on dual-person mode to generate a dyadic structural report.
              </div>
            )}

            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
              <div className="mb-3 flex items-center gap-2 text-lg font-semibold text-slate-900">
                <FileText className="h-5 w-5" /> Generated description
              </div>
              <div className="text-sm leading-7 text-slate-700">{generatedDescription}</div>
            </div>

            <div className="rounded-3xl border border-slate-200 bg-white/80 p-5 shadow-sm backdrop-blur">
              <div className="mb-3 text-base font-semibold text-slate-900">Optional researcher / user note</div>
              <Textarea
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Add narrative observations here. This can later be integrated with text-based interpretation."
                className="min-h-[120px] rounded-2xl"
              />
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
