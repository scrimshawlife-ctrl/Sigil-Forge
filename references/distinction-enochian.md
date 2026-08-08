# Distinction: intent sigils vs Enochian and Goetic seals

## Why this file exists

Operators and agents must **not collapse** Enochian seals, Goetic / Solomonic
spirit seals, or other **authority / placement** seal systems into Spare-style
**intent sigils**. Different crafts, different jobs, different authorities.

Namespace and future interop boundaries:
`authority-seal-namespace.md`.

## Intent sigils (Sigil-Forge domain)

| Aspect | Intent sigil |
|--------|----------------|
| Purpose | Compress and multi-encode a **statement of desire / focus** |
| Methods | Spare monogram + kamea path fusion + modern digest/stego |
| Framing | Creative tool or personal symbolic practice |
| Product | Forge packet + procedural master glyph |
| Efficacy | **Never claimed** |
| Default forge | **Yes** — core `construct` / wizard product |

## Enochian seals (not Sigil-Forge default)

| Aspect | Enochian / authority seals |
|--------|----------------------------|
| Purpose | Names, tablets, authority, placement, hierarchical spirit work as treated in their own systems |
| Methods | Distinct letter tables, watchtower / tablet logic, seal construction traditions |
| Framing | Not interchangeable with chaos monograms |
| Product | Not produced by this skill’s default forge |
| Ownership | e.g. separate Hermes skill or opt-in authority namespace (see `authority-seal-namespace.md`) |
| Detection | Language such as *enochian*, *watchtower* → `enochian_seal` family; construct/wizard **refuse** |

## Goetic seals (not Sigil-Forge default)

| Aspect | Goetic / Solomonic spirit seals |
|--------|----------------------------------|
| Purpose | Entity identifiers and hierarchical spirit work as treated in Goetia / Solomonic traditions |
| Methods | Named spirit seals, manuscript and print-tradition geometries — **not** Spare reduction or kamea intent paths |
| Framing | Not interchangeable with intent monograms or Agrippan **planetary** plate characters |
| Product | Not produced by this skill’s default forge |
| Ownership | Separate skill or future corpus-backed opt-in module only — never silent invent |
| Detection | Language such as *goetic*, *goetia*, *ars goetia*, *solomonic (spirit) seal* → `goetic_seal`; construct/wizard **refuse** |

**Do not confuse** with opt-in **planetary** seals (`--planetary-seal`): those are
Agrippan planetary character geometry (plate / name-on-kamea / reconstruct) in
this skill’s craft channels. They are **not** Goetic spirit seals and must not
be labeled as such.

## Rules for agents

1. If the user asks for an **Enochian seal**, do **not** silently emit a Spare/kamea
   intent glyph and call it Enochian.
2. If the user asks for a **Goetic / Solomonic spirit seal**, do **not** emit an
   intent glyph (or planetary plate) and rebrand it as Goetic.
3. If the user wants an **intent sigil**, use Sigil-Forge; do not require Enochian
   or Goetic tables.
4. Optional future interop (`intent_token`, `sigil_glyph`) may **name** related
   artifacts without merging geometries or doctrines.
5. Cultural or closed-practice boundaries stated by the operator override channel
   enthusiasm — skip or refuse rather than invent.
6. On engine refusal (`AUTHORITY_SEAL_EXCLUDED` / wizard `refused: true`): explain
   the distinction, point to this file and `authority-seal-namespace.md`, invite a
   present-tense intent rewrite. Write **no** forge artifacts.

## Related non-goals (default forge)

- Bind-runes and Rose Cross as **required** channels (they are attempted carriers;
  not authority-seal systems)
- Full ritual liturgy or banishing systems
- Treating stego carriers as spirit-authority tokens
- Auto-emitting or inventing manuscript Goetic/Enochian geometry

## Related

- Namespace: `authority-seal-namespace.md`
- Safety: `safety-and-framing.md`
- Expansion: `expansion-spine.md`
- Skill contract: `../SKILL.md`
