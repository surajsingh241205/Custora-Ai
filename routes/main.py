from flask import Blueprint, render_template, request, send_file, jsonify
from flask_login import login_required
from services.prediction import predict_churn
from services.ai_summary import generate_ai_summary
from services.pdf_report import generate_pdf_report
import os

main_bp = Blueprint("main", __name__)

UPLOAD_FOLDER = "uploads"


@main_bp.route("/")
def home():
    return render_template("landing.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@main_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        file = request.files["file"]

        if file.filename == "":
            return "No file selected"

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        result_df, _ = predict_churn(filepath)

        full_result_path = os.path.join(UPLOAD_FOLDER, "full_results.csv")
        result_df.to_csv(full_result_path, index=False)

        high = int((result_df["Risk_Level"] == "High Risk").sum())
        medium = int((result_df["Risk_Level"] == "Medium Risk").sum())
        low = int((result_df["Risk_Level"] == "Low Risk").sum())
        total = int(len(result_df))

        preview_df = result_df.head(10)

        return render_template(
            "results.html",
            tables=preview_df.to_dict(orient="records"),
            columns=list(preview_df.columns),
            high=high,
            medium=medium,
            low=low,
            total=total
        )

    return render_template("upload.html")


@main_bp.route("/generate_ai", methods=["POST"])
@login_required
def generate_ai():

    data = request.json

    total = int(data.get("total", 0))
    high = int(data.get("high", 0))
    medium = int(data.get("medium", 0))
    low = int(data.get("low", 0))

    high_pct = round((high / total) * 100, 2) if total else 0
    medium_pct = round((medium / total) * 100, 2) if total else 0
    low_pct = round((low / total) * 100, 2) if total else 0

    ai_summary = generate_ai_summary(
        total,
        high_pct,
        medium_pct,
        low_pct
    )

    return jsonify(ai_summary)


@main_bp.route("/download/pdf", methods=["POST"])
@login_required
def download_pdf():

    try:
        data = request.json

        total = int(data.get("total", 0))
        high = int(data.get("high", 0))
        medium = int(data.get("medium", 0))
        low = int(data.get("low", 0))
        ai_summary = data.get("ai_summary", {})
        chart_image = data.get("chart_image", None)

        pdf_path = os.path.join(UPLOAD_FOLDER, "custora_ai_report.pdf")

        generate_pdf_report(
            pdf_path,
            total,
            high,
            medium,
            low,
            ai_summary,
            chart_image
        )

        return send_file(pdf_path, as_attachment=True)

    except Exception as e:
        print("PDF ERROR:", e)
        return "PDF generation failed", 500


@main_bp.route("/download/csv")
@login_required
def download_csv():
    path = os.path.join(UPLOAD_FOLDER, "full_results.csv")
    return send_file(path, as_attachment=True)
