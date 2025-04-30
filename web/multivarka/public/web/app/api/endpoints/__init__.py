from .analysis import router as analysis
from .job import router as job
from .ping import router as ping
from .upload import router as upload
from .table import router as table

routers = [ping, upload, analysis, job, table]
