import re

from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from base.models import Link
from datasources.models import DataSource, SourceSubdivision


def process_links(row, dua_column_name="DUA", link_column_name="Link"):
    links = []
    row["Links"] = ""
    if row[dua_column_name]:
        link, _ = Link.objects.get_or_create(
            url=row[dua_column_name], defaults={"link_type": "DUA"}
        )
        links.append(link.id)
    if row[link_column_name]:
        # Regular expression to find URLs
        url_pattern = re.compile(r"\[(.*?)\]\((.*?)\)")
        # Find all matches
        matches = url_pattern.findall(row[link_column_name])
        if not matches:
            link, _ = Link.objects.get_or_create(
                url=row[link_column_name], defaults={"link_type": "Related Link"}
            )
            links.append(link.id)
        else:
            for match in matches:
                link, _ = Link.objects.get_or_create(
                    url=match[1],
                    defaults={
                        "link_type": match[0],
                    },
                )
                links.append(link.id)
    row["Links"] = links


def process_datasource_name(row):
    if row["Name"]:
        row["Name"] = row["Name"].capitalize()


def process_datasources(row):
    datasource, _ = DataSource.objects.get_or_create(
        name=row["DB Source"],
        defaults={
            "display_name": row["Name"],
            "description": row["Description"],
            "license": row["License"],
        },
    )
    for link in row["Links"]:
        datasource.related_links.add(link)


class SourceSubdivisionResource(resources.ModelResource):
    """
    Resource for the SourceSubdivision model.
    """

    name = Field(attribute="name", column_name="Source Subdivision")
    display_name = Field(attribute="display_name", column_name="External Name")
    data_source = Field(
        column_name="DB Source",
        attribute="data_source",
        widget=ForeignKeyWidget(DataSource, field="name"),
    )

    class Meta:
        model = SourceSubdivision
        fields = ("name", "display_name", "data_source")
        import_id_fields: list[str] = [
            "name",
        ]
        skip_unchanged = True

    def before_import_row(self, row, **kwargs):
        process_datasource_name(row)
        process_links(row)
        process_datasources(row)
