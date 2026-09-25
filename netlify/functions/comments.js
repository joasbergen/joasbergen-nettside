const { getStore, connectLambda } = require("@netlify/blobs");

exports.handler = async (event) => {
  connectLambda(event);
  const params = event.queryStringParameters || {};
  const slug = params.slug;
  if (!slug) return { statusCode: 400, body: "Mangler slug" };
  const store = getStore("kommentarer");

  if (event.httpMethod === "GET") {
    const liste = (await store.get(slug, { type: "json" })) || [];
    return { statusCode: 200, headers: { "Content-Type": "application/json" }, body: JSON.stringify(liste) };
  }

  if (event.httpMethod === "POST") {
    let data;
    try {
      data = JSON.parse(event.body || "{}");
    } catch {
      return { statusCode: 400, body: "Ugyldig data" };
    }
    if (data.kbot) return { statusCode: 200, headers: { "Content-Type": "application/json" }, body: "{}" };
    const navn = String(data.navn || "").trim().slice(0, 80);
    const tekst = String(data.tekst || "").trim().slice(0, 2000);
    if (!navn || !tekst) return { statusCode: 400, body: "Navn og kommentar må fylles ut" };
    const liste = (await store.get(slug, { type: "json" })) || [];
    const kommentar = {
      id: Date.now().toString(36) + Math.random().toString(36).slice(2, 8),
      navn,
      tekst,
      dato: new Date().toLocaleDateString("nb-NO", { day: "numeric", month: "long", year: "numeric" }),
    };
    liste.push(kommentar);
    await store.setJSON(slug, liste);
    return { statusCode: 200, headers: { "Content-Type": "application/json" }, body: JSON.stringify(kommentar) };
  }

  if (event.httpMethod === "DELETE") {
    const passord = process.env.KOMMENTAR_PASSORD;
    const auth = event.headers.authorization || event.headers.Authorization || "";
    if (!passord || auth !== `Bearer ${passord}`) {
      return { statusCode: 401, body: "Feil passord" };
    }
    const id = params.id;
    if (!id) return { statusCode: 400, body: "Mangler id" };
    const liste = (await store.get(slug, { type: "json" })) || [];
    const ny = liste.filter((k) => k.id !== id);
    await store.setJSON(slug, ny);
    return { statusCode: 200, headers: { "Content-Type": "application/json" }, body: "{}" };
  }

  return { statusCode: 405, body: "Metode ikke støttet" };
};
