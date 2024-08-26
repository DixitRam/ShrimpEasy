# build_files.sh
pip install -r requirements.txt

# make migrations
pip install --upgrade pip
python manage.py migrate 
python manage.py collectstatic --no-input
echo "🎉🎉🎉 Done 🎉🎉🎉"
